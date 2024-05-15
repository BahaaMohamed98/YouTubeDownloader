import tkinter
from tkinter import filedialog
from pytube import YouTube
import customtkinter
import pyperclip
import os


downloading = False


# function to download video
def downloadVideo():
    downloading = True
    try:
        yt = YouTube(video_url.get(), on_progress_callback=on_progress)
        video = (
            yt.streams.filter(res=optionMenu.get()).first()
            if optionMenu.get() != "Audio only"
            else yt.streams.filter(only_audio=True).first()
        )

        progressBar.set(0)
        # progressBar.update()

        progressLabel.configure("0%")
        # progressLabel.update()

        title.configure(text=video.title)
        # title.update()

        input.configure(border_color="white", text_color="white")
        # input.update()

        infoLabel.configure(text="")
        # infoLabel.update()

        if optionMenu.get() == "Audio only":
            video.download(downloadLocation.get(), filename=yt.title + ".mp3")
        else:
            video.download(downloadLocation.get())

        infoLabel.configure(text="Download complete", text_color="white")
    except:
        infoLabel.configure(text="Failed to download", text_color="red")
        input.configure(border_color="red", text_color="red")
    downloading = False


# updates progress bar and label bar while downloading
def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    completion_percentage = int(bytes_downloaded / total_size * 100)

    # update progress label
    progressLabel.configure(text=str(completion_percentage) + "%")
    progressLabel.update()

    # update progress bar
    progressBar.set(float(completion_percentage) / 100)
    progressBar.update()


#  pastes clipboard content into the URL input field
def paste():
    video_url.set(pyperclip.paste())
    validate_url()


# Function to reset progress bar to 0
def reset_progress():
    title.configure(text="Insert YouTube URL")
    progressBar.set(0)
    progressLabel.configure(text="0%")
    infoLabel.configure(text="")
    infoLabel.configure(text="", text_color="white")
    input.configure(border_color="white", text_color="white")


# validates the url in the input
def validate_url():
    if not downloading:
        url = video_url.get()
        if url.startswith("http") or url == "":
            reset_progress()
        else:
            input.configure(border_color="red", text_color="red")


# to browse for download location
def browseFiles():
    download_dir = filedialog.askdirectory()
    if download_dir:
        downloadLocation.set(download_dir)


# system settings
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# font
font = ("sans-serif", 16, "bold")


# app frame
app = customtkinter.CTk()
app.geometry("570x400")
app.title("YouTube Downloader")
app.iconbitmap("icon.ico")


# adding UI elements

# title
title = customtkinter.CTkLabel(
    app, text="Insert YouTube URL", text_color="white", font=("sans-serif", 21, "bold")
)  # TODO fix the paste button
title.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

# input frame
input_frame = customtkinter.CTkFrame(app)
input_frame.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)


# URL input
video_url = tkinter.StringVar()
input = customtkinter.CTkEntry(
    input_frame,
    width=350,
    height=40,
    font=font,
    corner_radius=8,
    textvariable=video_url,
    placeholder_text="https://",
    border_color="white",
)
input.pack(side="left", padx=5)

# Bind the reset_progress function to the Entry widget
input.bind("<KeyRelease>", lambda event: validate_url())

# paste button
pasteButton = customtkinter.CTkButton(
    input_frame, text="Paste", corner_radius=8, command=paste, font=font
)
pasteButton.pack(side="right", padx=5)


# progress frame
progress_frame = customtkinter.CTkFrame(app)
progress_frame.place(relx=0.5, rely=0.45, anchor=tkinter.CENTER)


# progress percentage
progressLabel = customtkinter.CTkLabel(progress_frame, text="0%", font=font)
progressLabel.pack(side="right", padx=5)


# progress bar
progressBar = customtkinter.CTkProgressBar(progress_frame, width=300)
progressBar.set(0)
progressBar.pack(side="left", padx=5)


downloadLocationLabel = customtkinter.CTkLabel(
    app, text="Download location:", font=font
)
downloadLocationLabel.place(relx=0.5, rely=0.6, anchor=customtkinter.CENTER)

# browse frame
browseFrame = customtkinter.CTkFrame(app)
browseFrame.place(relx=0.5, rely=0.7, anchor=customtkinter.CENTER)

downloadLocation = customtkinter.StringVar()

# browse files button
browseFilesButton = customtkinter.CTkButton(
    browseFrame, text="Browse files", command=browseFiles, font=font, width=50
)
downloadLocation.set(os.getcwd())
browseFilesButton.pack(side="right", padx=5)


# download location text entry
downloadEntry = customtkinter.CTkEntry(
    browseFrame, textvariable=downloadLocation, width=300, font=font
)
downloadEntry.pack(side="left", padx=5)


# download frame
downloadFrame = customtkinter.CTkFrame(app)
downloadFrame.place(relx=0.5, rely=0.85, anchor=tkinter.CENTER)

# download button
DownloadButton = customtkinter.CTkButton(
    downloadFrame,
    text="Download",
    corner_radius=8,
    command=downloadVideo,
    font=font,
)
DownloadButton.pack(side="left", padx=5)

# drop-down for choosing quality
optionMenu = customtkinter.CTkOptionMenu(
    downloadFrame,
    width=80,
    values=["720p", "360p", "Audio only"],
    font=font,
    dropdown_font=font,
)
optionMenu.pack(side="right", padx=5)


# infoLabel
infoLabel = customtkinter.CTkLabel(
    app,
    text="",
    text_color="white",
    font=font,
)
infoLabel.place(relx=0.5, rely=0.95, anchor=tkinter.CENTER)

# main loop
app.mainloop()
