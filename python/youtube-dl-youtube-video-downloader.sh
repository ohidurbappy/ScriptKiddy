#print welcome message
# must install youtube-dl in python virtualenv venv 
echo "Youtube Video Downloader"
echo "v0.0.9"


source $PWD/venv/bin/activate


echo "Select an Option"
echo "1.Download a video"
echo "2.Download a playlist"
echo "your choice:"
read option

if [ $option -eq 1 ];
then
echo "Enter Video URL:"
read url
`youtube-dl -o '~/Videos/%(title)s.%(ext)s' $url`
else
echo "Enter Video URL:"
read url
`youtube-dl -o '~/Videos/%(playlist)s/%(playlist_index)s - %(title)s.%(ext)s' $url`
fi


echo "Downloading Fininshed"






