import os
import shutil
import logging
    
def copy_file(copy_path, dest_path):
    file = os.path.isfile(dest_path)
    if file:
        logging.info(dest_path + " exists")
    
    else:
        logging.warning(dest_path + " does not exist")
        shutil.copyfile(copy_path, dest_path)
        logging.info(dest_path + " created from " + copy_path)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    copy_file(".env.sample", ".env")
    copy_file("profiles.yml.sample", "profiles.yml")