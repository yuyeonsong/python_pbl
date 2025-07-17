import ftplib

def login_clear(ftpip, ftpid, ftppw):
    try:
        ftp = ftplib.FTP(ftpip)
        ftp.login(ftpid, ftppw)

        current_dir = ftp.pwd()
        file_list = []
        ftp.retrlines('LIST', file_list.append)
        file_name_list = ftp.nlst()

        ftp.quit()

        return {
            "success": True,
            "current_dir": current_dir,
            "file_list": file_list,
            "file_name_list": file_name_list
        }

    except ftplib.all_errors as e:
        return {
            "success": False,
            "error": str(e)
        }