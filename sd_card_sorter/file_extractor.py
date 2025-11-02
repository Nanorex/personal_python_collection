import os
import shutil


class Keywords:
    Images = "Images"
    Videos = "Videos"
    Documents = "Documents"
    Music = "Music"
    Unknown = "Unknown"

    ImageTypes = ["png", "jpg", "bmp", "gif", "jpeg"]
    VideoTypes = ["mp4", "mov", "avi"]
    MusicTypes = ["flac", "mp3", "wav", "aac", "aiff"]
    DocumentTypes = ["pdf", "doc", "docx", "txt", "ppt", "pptx"]

    Categories = [Images, Videos, Documents, Music, Unknown]


def prepare_output(targe_path, keyword_class):
    if os.path.exists(targe_path):
        shutil.rmtree(targe_path)
    os.mkdir(targe_path)
    for keyword in keyword_class.Categories:
        os.mkdir(os.path.join(targe_path, keyword))


def categorize_folder(folder_path):
    keywords = Keywords()
    files_dict = {}
    for keyword in keywords.Categories:
        files_dict[keyword] = []


    for root, dirs, files in os.walk(folder_path):
        for file in files:
            full_path = os.path.join(root, file)
            size = os.path.getsize(full_path)
            suffix = file.split(".")[-1].lower()

            if suffix in keywords.ImageTypes:
                files_dict[keywords.Images].append(full_path)
            elif suffix in keywords.VideoTypes:
                files_dict[keywords.Videos].append(full_path)
            elif suffix in keywords.MusicTypes:
                files_dict[keywords.Music].append(full_path)
            elif suffix in keywords.DocumentTypes:
                files_dict[keywords.Documents].append(full_path)
            elif (size / 1024) > 1000:
                files_dict[keywords.Unknown].append(full_path)

    return files_dict

if __name__ == "__main__":
    input_path = r"G:\Bianca_SD_karte"
    output_path = r"G:\Bianca_SDKarte_Sortiert"

    prepare_output(output_path, Keywords())
    cat_dict = categorize_folder(input_path)


            #print(f"Found file {file} with a size of {size / 1024:.1f} kB")

    print("Searching done, starting copying")
    """overall_counter = 0
    for keyword in keywords.Categories:
        full_out_path = os.path.join(output_path, keyword)
        for source_path in files_dict[keyword]:
            filename = f"{overall_counter:05d}_{os.path.basename(source_path)}"
            shutil.copy(source_path, os.path.join(full_out_path, filename))
            overall_counter += 1
            if overall_counter % 1000 == 0:
                print(f"Processed {overall_counter} files")"""
