import os
import csv
import hashlib
import sys


def md5Checksum(filePath):
    with open(filePath, 'rb') as f:
        m = hashlib.md5()
        while True:
            data = f.read(4096)
            if not data:
                break
            m.update(data)
        return m.hexdigest()

def generateScan(startpath, logdir):
    #print(logdir + 'scan_file.csv')
    with open(logdir + 'scan_file.csv', mode='w') as scan_file:
        line_writer = csv.writer(scan_file, delimiter=',')
        line_writer.writerow(['file_path','bytes','md5'])
        for root, dirs, files in os.walk(startpath):
            for f in files:
                #print(os.path.join(root, f), os.path.getsize(os.path.join(root, f)), md5Checksum(os.path.join(root, f)))
                line_writer.writerow([os.path.join(root, f), os.path.getsize(os.path.join(root, f)), md5Checksum(os.path.join(root, f))])

def generateBaseline(startpath, logdir):
    print("Creating baseline: " + logdir + "baseline_file.csv")
    with open(logdir + 'baseline_file.csv', mode='w') as baseline_file:
        line_writer = csv.writer(baseline_file, delimiter=',')
        line_writer.writerow(['file_path','bytes','md5'])
        for root, dirs, files in os.walk(startpath):
            for f in files:
                #print(os.path.join(root, f), os.path.getsize(os.path.join(root, f)), md5Checksum(os.path.join(root, f)))
                line_writer.writerow([os.path.join(root, f), os.path.getsize(os.path.join(root, f)), md5Checksum(os.path.join(root, f))])

def searchMD5(md5input, logdir):
    filesdb = [i for i in csv.DictReader(open(logdir + 'baseline_file.csv'), delimiter=',')]
    for row in filesdb:
        if row["md5"] == md5input:
            return True

def searchBasePath(pathinput, logdir):
    filesdb = [i for i in csv.DictReader(open(logdir + 'baseline_file.csv'), delimiter=',')]
    for row in filesdb:
        if row["file_path"] == pathinput:
            return True

def searchScanPath(pathinput, logdir):
    filesdb = [i for i in csv.DictReader(open(logdir + 'scan_file.csv'), delimiter=',')]
    for row in filesdb:
        if row["file_path"] == pathinput:
            return True

def getBaselineSize(pathinput, logdir):
    filesdb = [i for i in csv.DictReader(open(logdir + 'baseline_file.csv'), delimiter=',')]
    for row in filesdb:
        if row["file_path"] == pathinput:
            return row["bytes"]

def getMD5Match(md5input, logdir):
    filesdb = [i for i in csv.DictReader(open(logdir + 'baseline_file.csv'), delimiter=',')]
    for row in filesdb:
        if row["md5"] == md5input:
            return row["md5"]

def getBaselinePath(md5input, logdir):
    filesdb = [i for i in csv.DictReader(open(logdir + 'baseline_file.csv'), delimiter=',')]
    for row in filesdb:
        if row["md5"] == md5input:
            return row["file_path"]

def getScannedTotal(logdir):
    with open(logdir + 'scan_file.csv',"r") as f:
        reader = csv.reader(f,delimiter = ",")
        data = list(reader)
        row_count = len(data)
        #we need to subtract 1 to account for csv column header
        return row_count-1


def runScan(logdir):
    total_modified = 0
    #Check for Deleted files
    with open(logdir + 'baseline_file.csv') as basecsv:
        basefile = csv.reader(basecsv, delimiter=',')
        next(basefile)
        for row in basefile:
            if searchScanPath(row[0],logdir):
                True
            else:
                #DELETED
                print("D {0}".format(row[0]))
                total_modified += 1

    #Check for New, Updated and Modified files
    with open(logdir + 'scan_file.csv') as csvfile:
        scanfile = csv.reader(csvfile, delimiter=',')
        next(scanfile)
        for row in scanfile:
            if searchBasePath(row[0], logdir):
                True
                #path match true
                if searchMD5(row[2], logdir):
                    True
                else:
                    #MD5 MISMATCH
                    print("U {0} {1} {2}".format(row[0], getBaselineSize(row[0], logdir), row[1]))
                    total_modified += 1
            else:
                print("N {0} {1}".format(row[0], row[1]))
                total_modified += 1
                if getMD5Match(row[2], logdir) == row[2]:
                    #MATCH
                    print("M {0} {1}".format(getBaselinePath(row[2], logdir), row[0]))

        print("Total files scanned: {0}".format(getScannedTotal(logdir)))
        print("Total files modified: {0}".format(total_modified))

def main():
    if len(sys.argv) > 1:
        dir = sys.argv[1]
        logdir = sys.argv[2]
        if not logdir.endswith("/"):
            logdir = logdir + "/"
    else:
        print("Missing scan and log dir, exiting")
        exit()

    if not os.path.exists(logdir + "/baseline_file.csv"):
        #print(logdir + "/baseline_file.csv")
        print("Baseline doesn't exist, creating")
        generateBaseline(dir, logdir)
    else:
        print("Scanning...")
        generateScan(dir, logdir)
        runScan(logdir)



if __name__ == "__main__":
    main()
