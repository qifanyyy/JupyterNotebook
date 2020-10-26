"""
    Created by mbenlioglu on 11/23/2017
"""
import os
import warnings
import subprocess
import sys
import time
import urllib2
import argparse


class ProgressBar:
    """
    Helper class to create a terminal progress bar
    """
    def __init__(self, total, prefix='', suffix='', decimals=1, bar_length=50, fill='#'):
        """
        Initialize the progressBar
        :param total:      (Required) total iterations, the goal
        :param prefix:     (Optional) prefix string that will show before the progress bar
        :param suffix:     (Optional) suffix string that will show after the progress bar
        :param decimals:   (Optional) positive number of decimals in percent compete
        :param bar_length: (Optional) character length of the progress bar
        :param fill:       (Optional) fill character of the progress bar representing the completed percentage
        """
        self.__completed = 0
        self.__total = float(total)
        self.__prefix = prefix
        self.__suffix = suffix
        self.__decimals = decimals
        self.__bar_length = bar_length
        self.__fill = fill

    def print_progress(self, progress):
        """
        Update the completed percentage and update the progress bar on the terminal
        :param progress: (Required) amount of progress
        """
        if self.__completed != self.__total:
            # update completed iteration count
            remaining = self.__total - self.__completed
            self.__completed = self.__completed + progress if (progress < remaining) else self.__total

            # create progress bar string and print
            str_format = "{0:." + str(self.__decimals) + "f}"
            percents = str_format.format(100 * self.__completed / self.__total)
            filled_length = int(self.__bar_length * self.__completed // self.__total)
            bar = self.__fill * filled_length + '-' * (self.__bar_length - filled_length)

            sys.stdout.write('\r%s |%s| %s%% %s' % (self.__prefix, bar, percents, self.__suffix))
        if self.__completed >= self.__total:
            sys.stdout.write('\n')
        sys.stdout.flush()


# extract all files stored in the archive
def extractall(archive_path, create_sub_folder=False, remove_archive=False, winrar_path='"C:/Program '
                                                                                        'Files/WinRAR/WinRAR.exe"'):
    basename = os.path.basename(archive_path)

    # error checks
    if not os.path.exists(archive_path):
        raise IOError('Archive does not exist')
    if os.path.isdir(archive_path):
        raise IOError('Given path is not an archive, but a directory')
    archive_types = ['.rar', '.zip', '.7z', '.ace', '.arc', '.bz2', '.cab', '.gz',
                     '.iso', '.jar', '.lzh', '.tar', '.uue', '.xz', '.z']
    if os.path.splitext(basename)[1] not in archive_types:
        raise ValueError('Unsupported archive...')

    sys_script = winrar_path + r' x -ibck -o+ '
    if not create_sub_folder:
        sys_script += '"' + archive_path + "\" *.* \"" + os.path.dirname(archive_path) + '"'
        if subprocess.Popen(sys_script).wait() != 0:
            print 'Something went wrong during extracting', archive_path
            return False
    else:
        dirname = os.path.splitext(basename)[0]
        new_path = os.path.join(os.path.dirname(archive_path), dirname)
        try:
            os.makedirs(new_path)
        except WindowsError:
            warnings.warn('Folder already exists! using the existing folder...', RuntimeWarning)

        sys_script += archive_path + " *.* " + new_path
        if subprocess.Popen(sys_script).wait() != 0:
            raise RuntimeError('Something went wrong during extracting ' + archive_path + ' create_folder = True')

    if remove_archive:
        os.remove(archive_path)

    time.sleep(0.01)
    return True


def download_file(url, dest_folder='.'):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    if not os.path.isdir(dest_folder):
        raise ValueError('Destination folder is not a folder!')

    # Get data
    try:
        data = urllib2.urlopen(url)
        metadata = data.info()
        file_name = os.path.join(dest_folder, os.path.basename(url))
        file_size = int(metadata.getheaders('Content-Length')[0])

        pb = ProgressBar(file_size, os.path.basename(url), 'Complete')
        pb.print_progress(0)
        with open(file_name, 'wb') as downloaded_file:
            chunk_size = 64 * 1024  # MB of data
            while True:
                buff = data.read(chunk_size)
                if not buff:
                    break
                downloaded_file.write(buff)
                pb.print_progress(len(buff))
    # handle errors
    except urllib2.HTTPError, e:
        print "HTTP Error:", e.code, url
    except urllib2.URLError, e:
        print "URL Error:", e.reason, url


def crawl(winrar_path='"C:/Program Files/WinRAR/WinRAR.exe"', remove_archives=False):
    urls = ["https://sparse.tamu.edu/MM/Schenk_AFE/af_shell3.tar.gz",
            "https://sparse.tamu.edu/MM/Oberwolfach/bone010.tar.gz",
            "https://sparse.tamu.edu/MM/DIMACS10/coPapersDBLP.tar.gz",
            "https://sparse.tamu.edu/MM/Newman/karate.tar.gz",
            "https://sparse.tamu.edu/MM/Schenk/nlpkkt120.tar.gz",
            "https://sparse.tamu.edu/MM/Schenk/nlpkkt240.tar.gz"]
    destination = './data/'

    for url in urls:
        download_file(url, destination)
        extractall(os.path.join(destination, os.path.basename(url)),
                   remove_archive=remove_archives, winrar_path=winrar_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-r', '--remove_archives', help='Boolean flag to determine whether to remove archives after '
                                                        'download or not', action='store_true')
    parser.add_argument('--winrar_path', help='Location to WinRAR.exe (with "quotations" if path contains spaces)',
                        default='"C:/Program Files/WinRAR/WinRAR.exe"')

    args = parser.parse_args()

    stripped = args.winrar_path.strip('"')
    if not os.path.exists(stripped) or os.path.isdir(stripped) or os.path.basename(stripped).lower() != 'winrar.exe':
        raise ValueError('Entered WinRAR path is wrong!')
    crawl(args.winrar_path, args.remove_archives)
