"""
Script to download and set up winutils.exe for Hadoop on Windows.
"""
import os
import sys
import urllib.request
import shutil
import zipfile
from pathlib import Path

def setup_winutils():
    """Download and set up winutils.exe for Hadoop on Windows."""
    try:
        # Set up paths
        spark_home = os.environ.get('SPARK_HOME', 'C:\\spark\\spark-3.5.4-bin-hadoop3')
        hadoop_home = spark_home  # Using Spark's Hadoop
        hadoop_bin = os.path.join(hadoop_home, 'bin')
        
        # Create bin directory if it doesn't exist
        os.makedirs(hadoop_bin, exist_ok=True)
        
        # Path for winutils.exe
        winutils_path = os.path.join(hadoop_bin, 'winutils.exe')
        
        if not os.path.exists(winutils_path):
            print("Downloading winutils.exe...")
            # URL for winutils.exe (using a version compatible with Hadoop 3.x)
            winutils_url = "https://github.com/cdarlint/winutils/raw/master/hadoop-3.2.2/bin/winutils.exe"
            
            # Download winutils.exe
            urllib.request.urlretrieve(winutils_url, winutils_path)
            print(f"Downloaded winutils.exe to {winutils_path}")
        else:
            print("winutils.exe already exists")
        
        # Set environment variables
        os.environ['HADOOP_HOME'] = hadoop_home
        os.environ['PATH'] = f"{hadoop_bin};{os.environ['PATH']}"
        
        print("\nHadoop environment set up successfully!")
        print(f"HADOOP_HOME: {hadoop_home}")
        print(f"winutils.exe location: {winutils_path}")
        return True
        
    except Exception as e:
        print(f"Error setting up Hadoop environment: {str(e)}")
        return False

if __name__ == "__main__":
    setup_winutils() 