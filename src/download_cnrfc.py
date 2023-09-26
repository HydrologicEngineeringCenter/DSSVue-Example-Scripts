import urllib
import zipfile
import os
from datetime import datetime, timedelta



def downloadAndUnzip(destination_directory,waterShedName,strDate):
# URL of the file to download
    #url = "https://www.cnrfc.noaa.gov/csv/2019092312_SanJoaquin_hefs_csv_hourly.zip"
    zipFileName =strDate+"_"+waterShedName+"_hefs_csv_hourly.zip"
    url = "https://www.cnrfc.noaa.gov/csv/"+zipFileName
    print("downloading :"+url)
    # Ensure the destination directory exists
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    # Destination file path where you want to save the downloaded ZIP file
    zip_file_path = os.path.join(destination_directory, zipFileName)

    try:
        # Open a connection to the URL and download the file
        urllib.urlretrieve(url, zip_file_path)
        print("File downloaded successfully!")

        # Unzip the downloaded file
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(destination_directory)
        print("File unzipped successfully!")

        # Clean up by removing the ZIP file
        #os.remove(zip_file_path)

    except Exception:
        print("An error occurred: reading and unziping '"+url+"'")


t = datetime(2023, 9, 26)
numDaysBack = 30
waterShedName = "SanJoaquin"
destination_directory = "c:/tmp/dwr"

for i in range(numDaysBack):
  # "2019092312_SanJoaquin_hefs_csv_hourly.zip"
  strDate = t.strftime("%Y%m%d12")
  downloadAndUnzip(destination_directory,waterShedName,strDate)
  t = t - timedelta(days=1)
