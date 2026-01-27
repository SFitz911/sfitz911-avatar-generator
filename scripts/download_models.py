#!/usr/bin/env python3
"""
SFitz911 Avatar Generator - Model Download Script
Downloads model weights from cloud storage (S3 or GCS)
"""

import os
import sys
from pathlib import Path
import boto3
from botocore.exceptions import ClientError
from tqdm import tqdm
import argparse


def download_from_s3(bucket: str, prefix: str, local_path: str, region: str = "us-east-1"):
    """
    Download models from AWS S3
    
    Args:
        bucket: S3 bucket name
        prefix: S3 prefix/path
        local_path: Local destination path
        region: AWS region
    """
    print(f"Downloading from S3: s3://{bucket}/{prefix}")
    print(f"Destination: {local_path}")
    
    # Initialize S3 client
    s3 = boto3.client('s3', region_name=region)
    
    # Create local directory
    Path(local_path).mkdir(parents=True, exist_ok=True)
    
    # List all objects
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket, Prefix=prefix)
    
    # Collect all files
    files = []
    for page in pages:
        if 'Contents' in page:
            files.extend(page['Contents'])
    
    if not files:
        print(f"⚠ No files found at s3://{bucket}/{prefix}")
        return
    
    print(f"Found {len(files)} files to download")
    
    # Download each file with progress bar
    for obj in tqdm(files, desc="Downloading"):
        key = obj['Key']
        size = obj['Size']
        
        # Skip directories
        if key.endswith('/'):
            continue
        
        # Calculate local path
        relative_path = key.replace(prefix, '').lstrip('/')
        local_file = os.path.join(local_path, relative_path)
        
        # Create parent directory
        Path(local_file).parent.mkdir(parents=True, exist_ok=True)
        
        # Download file
        try:
            s3.download_file(bucket, key, local_file)
            tqdm.write(f"  ✓ {relative_path} ({size / 1024 / 1024:.1f} MB)")
        except ClientError as e:
            tqdm.write(f"  ✗ Failed to download {relative_path}: {e}")
    
    print("\n✓ Download complete!")


def download_from_gcs(bucket: str, prefix: str, local_path: str):
    """
    Download models from Google Cloud Storage
    
    Args:
        bucket: GCS bucket name
        prefix: GCS prefix/path
        local_path: Local destination path
    """
    try:
        from google.cloud import storage
    except ImportError:
        print("Error: google-cloud-storage not installed")
        print("Install with: pip install google-cloud-storage")
        sys.exit(1)
    
    print(f"Downloading from GCS: gs://{bucket}/{prefix}")
    print(f"Destination: {local_path}")
    
    # Initialize GCS client
    client = storage.Client()
    bucket_obj = client.bucket(bucket)
    
    # Create local directory
    Path(local_path).mkdir(parents=True, exist_ok=True)
    
    # List all blobs
    blobs = list(bucket_obj.list_blobs(prefix=prefix))
    
    if not blobs:
        print(f"⚠ No files found at gs://{bucket}/{prefix}")
        return
    
    print(f"Found {len(blobs)} files to download")
    
    # Download each file with progress bar
    for blob in tqdm(blobs, desc="Downloading"):
        # Skip directories
        if blob.name.endswith('/'):
            continue
        
        # Calculate local path
        relative_path = blob.name.replace(prefix, '').lstrip('/')
        local_file = os.path.join(local_path, relative_path)
        
        # Create parent directory
        Path(local_file).parent.mkdir(parents=True, exist_ok=True)
        
        # Download file
        try:
            blob.download_to_filename(local_file)
            tqdm.write(f"  ✓ {relative_path} ({blob.size / 1024 / 1024:.1f} MB)")
        except Exception as e:
            tqdm.write(f"  ✗ Failed to download {relative_path}: {e}")
    
    print("\n✓ Download complete!")


def main():
    parser = argparse.ArgumentParser(
        description="Download LongCat model weights from cloud storage"
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
        default="models/longcat/",
        help="Path prefix in bucket (default: models/longcat/)"
    )
    parser.add_argument(
        "--output",
        default="./models/longcat",
        help="Local output directory (default: ./models/longcat)"
    )
    parser.add_argument(
        "--region",
        default="us-east-1",
        help="AWS region (only for S3, default: us-east-1)"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("SFitz911 Avatar Generator - Model Downloader")
    print("=" * 60)
    
    try:
        if args.provider == "s3":
            download_from_s3(
                bucket=args.bucket,
                prefix=args.prefix,
                local_path=args.output,
                region=args.region
            )
        elif args.provider == "gcs":
            download_from_gcs(
                bucket=args.bucket,
                prefix=args.prefix,
                local_path=args.output
            )
    except Exception as e:
        print(f"\n✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
