from PIL import Image
import os
import fillchar
from tkinter import Tk, filedialog
import webbrowser


errored_images = []
img_extensions = []
name_cnt, ext_cnt = 0, 0


def get_username():
    '''Function to get the username from the system'''
    if os.name == 'posix':
        for user, name in os.environ.items():
            if user == "USERNAME":
                return name
    else:
        for user, name in os.environ.items():
            if user == "USER":
                return name


def apply_edits_main(image_folder, selected_images, finalized_edit_selection):
    '''Main function of the module conaining all the functions'''
    target_folder = select_target_folder()
    apply_edits(selected_images, image_folder,
                finalized_edit_selection, target_folder)
    if len(errored_images) != 0:
        print("Some images may not be processed, will be saved in \"target_folder/Unprocessed Image\"")
    open_target_folder(target_folder)


def select_target_folder():
    '''Select target folder to save images'''
    user_name = get_username()
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    while True:
        fillchar.main_menu(" Apply Edits Menu ")
        user_choice = input(
            f"1. Select DIR to save images\n2. Continue with default DIR (User)\n{fillchar.draw_line()}\nUSER:")
        if user_choice == '1':
            target_folder = filedialog.askdirectory()
            if target_folder:
                print(
                    f"{fillchar.draw_line()}\nAll edited images will be saved to {target_folder}")
                break
        elif user_choice == '2':
            if os.name == "posix":
                target_folder = f"/home/{user_name}/IPEdits"
            else:
                target_folder = f"C:/Users/{user_name}/IPEdits"
            if not os.path.exists(target_folder):
                os.mkdir(target_folder)
                break
            else:
                break
        else:
            fillchar.in_between("Enter a valid choice")
            continue
        print("Target folder inside select_target_folder", target_folder)
    return target_folder


def apply_edits(selected_images, image_folder, selected_edits, target_folder):
    '''Apply selected edits to images one by one'''
    os.chdir(image_folder[0])
    image_filters = selected_edits[0]
    image_enhancements = selected_edits[1]
    image_resize = selected_edits[2]
    file_format, img_extensions = get_format(selected_images)
    fillchar.sub_menu("Saving in progress. Please wait...")
    print("Images will be saved to =>", target_folder)
    for image in selected_images:
        image = Image.open(image)
        try:
            if len(image_filters) != 0:
                image = apply_filters(image, image_filters)

            if len(image_enhancements) != 0:
                image = apply_enhancements(image, image_enhancements)

            if len(image_resize) != 0:
                image = apply_size(image, image_resize)
        except:
            pass
        save_images(image, selected_images, file_format,
                    img_extensions, target_folder, image_folder)
        image.close()


def save_images(image, selected_images, file_format, image_extesnsions, target_folder, image_folder):
    '''Save images to the specified target folder'''
    global name_cnt, ext_cnt
    image_name = selected_images[name_cnt]
    image_name = '.'.join(image_name.split('.')[:-1])
    name_cnt += 1
    if file_format == 'Default':
        extension = image_extesnsions[ext_cnt]
        ext_cnt += 1
    else:
        extension = file_format
    try:
        image.save(f"{target_folder}/{image_name}.{extension}")
    except:
        image_name = f"{image_name}.{file_format}"
        if image_name in os.listdir(f"{target_folder}"):
            os.remove(f"{target_folder}/{image_name}")
        unprocessed_image(target_folder, selected_images, image_name, image)


def unprocessed_image(target_folder, selected_images, image_name, image):
    '''Exception handling for images which cannot be saved using user settings will be saved as copy 
        in 'Unprocessed Images' folder in target folder'''
    errored_image_folder = "Unprocessed Images"
    if not os.path.exists(f"{target_folder}/{errored_image_folder}"):
        os.mkdir(f"{target_folder}/{errored_image_folder}")
        image_name = '.'.join(image_name.split('.')[:-1])
        for x in selected_images:
            extension = str(x).split('.')[1]
            x = '.'.join(x.split('.')[:-1])
            if x == image_name:
                image.save(
                    f"{target_folder}/{errored_image_folder}/{image_name}.{extension}")


def open_target_folder(target_folder):
    '''Open target folder to view saved images once all the tasks are completed'''
    while True:
        user_choice = input(f"{fillchar.draw_line()}\nDo you want to open target folder?\n{fillchar.draw_line()}"
                            f"\nUSER(Y/N): ").lower()
        if user_choice == 'y':
            webbrowser.open(target_folder)
            break
        elif user_choice == 'n':
            break
        else:
            fillchar.in_between("Enter a valid choice")


def apply_filters(image, image_filters):
    '''Function to apply selected filters to selected images'''
    for filters in image_filters:
        image = image.filter(filters)
    return image


def apply_enhancements(image, image_enhancements):
    '''Function to apply selected enhancements to selected  images'''
    for enhancement, val in image_enhancements.items():
        image = enhancement(image)
        image = image.enhance(val)
    return image


def apply_size(image, image_resize):
    '''Function to resize and create thumbnail of the images'''
    img_size_flag = [x for x in image_resize.keys()][0]
    img_size = [x for x in image_resize.values()][0]
    img_width = int(img_size[0])
    img_height = int(img_size[1])
    img_size = (img_width, img_height)
    if img_size_flag == 'Thumbnail':
        image.thumbnail(img_size, Image.ANTIALIAS)
    else:
        image = image.resize(img_size)
    return image


def get_format(selected_images):
    '''Function to get desired output image format for selected images'''
    file_format = ""
    while True:
        fillchar.sub_menu(" Image Format Selector ")
        user_choice = input(
            f"1. PNG\n2. JPEG\n3. JPG\n4. Default\n{fillchar.draw_line()}\nUSER:")
        if user_choice == '1':
            file_format = "png"
        elif user_choice == '2':
            file_format = "jpeg"
        elif user_choice == '3':
            file_format = "jpg"
        elif user_choice == '4':
            file_format = 'Default'
        else:
            print("Enter a valid choice!")
            continue
        break
    for image in selected_images:
        img_extensions.append(str(image).split('.')[-1])
    return file_format, img_extensions


if __name__ == "__main__":
    apply_edits_main(image_folder=[], selected_images=[],
                     finalized_edit_selection={})
