import pytube

def showCompletion(stream, file_handle):
    print("Download Complete")
    return
def show_progress_bar(stream, chunk, file_handle, bytes_remaining):
    print("#",end='',flush=True)
    return


video_url=input("Enter a url:")
yt=pytube.YouTube(video_url)
yt.register_on_progress_callback(show_progress_bar)
yt.register_on_complete_callback(showCompletion)
yt.streams.first().download('C:\\Users\Bappy\\Desktop\\')

ex=input("Press a key to Exit")



