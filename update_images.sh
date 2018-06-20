echo 'Mounting CIFS and loading images'

umount -a -t cifs -l
rm -rf /home/debian/Desktop/shared
mkdir /home/debian/Desktop/shared
mount -t cifs //stnls02.lnls.br/CommonSystems_Sirius/BEAGLETemp/ /home/debian/Desktop/shared/ -o username=$1,password=$2

echo 'Images have been loaded'

sudo cp -r /home/debian/Desktop/shared/ /home/debian/Desktop/downloads
echo 'Images have been copied to local directory'

exit 0

