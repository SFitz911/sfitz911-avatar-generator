#!/usr/bin/env python3
"""
SFitz911 Avatar Generator - Output Sync Script
Syncs generated videos to cloud storage before destroying instance
"""

import os
import sys
from pathlib import Path
import boto3
from botocore.exceptions import ClientError
from tqdm import tqdm
import argparse
from datetime import datetime


def sync_to_s3(local_path: str, bucket: str, prefix: str, region: str = "us-east-1", delete_local: bool = False):
    """
    Sync outputs to AWS S3
    
    Args:
        local_path: Local directory to sync
        bucket: S3 bucket name
        prefix: S3 prefix/path
        region: AWS region
        delete_local: Delete local files after successful upload
    """
    print(f"Syncing to S3: s3://{bucket}/{prefix}")
    print(f"Source: {local_path}")
    
    # Initialize S3 client
    s3 = boto3.client('s3', region_name=region)
    
    # Find all video files
    video_files = []
    for ext in ['*.mp4', '*.avi', '*.mov', '*.mkv']:
        video_files.extend(Path(local_path).glob(ext))
    
    if not video_files:
        print(f"⚠ No video files found in {local_path}")
        return
    
    print(f"Found {len(video_files)} video files to upload")
    
    # Upload each file with progress bar
    uploaded = []
    for file_path in tqdm(video_files, desc="Uploading"):
        relative_path = file_path.name
        s3_key = f"{prefix.rstrip('/')}/{relative_path}"
        
        try:
            # Check if file already exists
            try:
                s3.head_object(Bucket=bucket, Key=s3_key)
                tqdm.write(f"  ⊙ {relative_path} (already exists, skipping)")
                continue
            except ClientError:
                pass  # File doesn't exist, proceed with upload
            
            # Upload file
            file_size = file_path.stat().st_size
            s3.upload_file(
                str(file_path),
                bucket,
                s3_key,
                ExtraArgs={'ContentType': 'video/mp4'}
            )
            tqdm.write(f"  ✓ {relative_path} ({file_size / 1024 / 1024:.1f} MB)")
            uploaded.append(file_path)
            
        except Exception as e:
            tqdm.write(f"  ✗ Failed to upload {relative_path}: {e}")
    
    print(f"\n✓ Upload complete! ({len(uploaded)} files uploaded)")
    
    # Delete local files if requested
    if delete_local and uploaded:
        print("\nDeleting local files...")
        for file_path in uploaded:
            try:
                file_path.unlink()
                print(f"  ✓ Deleted {file_path.name}")
            except Exception as e:
                print(f"  ✗ Failed to delete {file_path.name}: {e}")


def sync_to_gcs(local_path: str, bucket: str, prefix: str, delete_local: bool = False):
    """
    Sync outputs to Google Cloud Storage
    
    Args:
        local_path: Local directory to sync
        bucket: GCS bucket name
        prefix: GCS prefix/path
        delete_local: Delete local files after successful upload
    """
    try:
        from google.cloud import storage
    except ImportError:
        print("Error: google-cloud-storage not installed")
        print("Install with: pip install google-cloud-storage")
        sys.exit(1)
    
    print(f"Syncing to GCS: gs://{bucket}/{prefix}")
    print(f"Source: {local_path}")
    
    # Initialize GCS client
    client = storage.Client()
    bucket_obj = client.bucket(bucket)
    
    # Find all video files
    video_files = []
    for ext in ['*.mp4', '*.avi', '*.mov', '*.mkv']:
        video_files.extend(Path(local_path).glob(ext))
    
    if not video_files:
        print(f"⚠ No video files found in {local_path}")
        return
    
    print(f"Found {len(video_files)} video files to upload")
    
    # Upload each file with progress bar
    uploaded = []
    for file_path in tqdm(video_files, desc="Uploading"):
        relative_path = file_path.name
        gcs_path = f"{prefix.rstrip('/')}/{relative_path}"
        
        try:
            # Check if file already exists
            blob = bucket_obj.blob(gcs_path)
            if blob.exists():
                tqdm.write(f"  ⊙ {relative_path} (already exists, skipping)")
                continue
            
            # Upload file
            file_size = file_path.stat().st_size
            blob.upload_from_filename(str(file_path), content_type='video/mp4')
            tqdm.write(f"  ✓ {relative_path} ({file_size / 1024 / 1024:.1f} MB)")
            uploaded.append(file_path)
            
        except Exception as e:
            tqdm.write(f"  ✗ Failed to upload {relative_path}: {e}")
    
    print(f"\n✓ Upload complete! ({len(uploaded)} files uploaded)")
    
    # Delete local files if requested
    if delete_local and uploaded:
        print("\nDeleting local files...")
        for file_path in uploaded:
            try:
                file_path.unlink()
                print(f"  ✓ Deleted {file_path.name}")
            except Exception as e:
                print(f"  ✗ Failed to delete {file_path.name}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Sync generated videos to cloud storage"
    )
    parser.add_argument(
        "--provider",
        choices=["s3", "gcs"],
        default="s3",
        help="Cloud storage provider (default: s3)"
    )
    parser.add_argument(
        "--bucket",
        required=True,
        help="Bucket name"
    )
    parser.add_argument(
        "--prefix",
        default=f"outputs/{datetime.now().strftime('%Y-%m-%d')}/",
        help="Path prefix in bucket (default: outputs/YYYY-MM-DD/)"
    )
    parser.add_argument(
        "--input",
        default="./outputs",
        help="Local input directory (default: ./outputs)"
    )
    parser.add_argument(
        "--region",
        default="us-east-1",
        help="AWS region (only for S3, default: us-east-1)"
    )
    parser.add_argument(
        "--delete-local",
        action="store_true",
        help="Delete local files after successful upload"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("SFitz911 Avatar Generator - Output Sync")
    print("=" * 60)
    print(f"Timestamp: {datetime.now().isoformat()}")
    print()
    
    try:
        if args.provider == "s3":
            sync_to_s3(
                local_path=args.input,
                bucket=args.bucket,
                prefix=args.prefix,
                region=args.region,
                delete_local=args.delete_local
            )
        elif args.provider == "gcs":
            sync_to_gcs(
                local_path=args.input,
                bucket=args.bucket,
                prefix=args.prefix,
                delete_local=args.delete_local
            )
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
