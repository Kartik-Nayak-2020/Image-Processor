from PIL import Image
import os
import fillchar
from tkinter import Tk, filedialog
import webbrowser


def get_username():
    for user, name in os.environ.items():
        if user == "USERNAME":
            return name


def apply_edits(image_folder, selected_images, selected_edits):
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
                print(f"All edited images will be saved to {target_folder}")
                print("Target inside if", target_folder)
                break
        elif user_choice == '2':
            print(os.name)
            input()
            if os.name == "posix":
                print("Linux")
                target_folder = f"/home/{user_name}/IPEdits"
            else:
                print("Windows")
                target_folder = f"C:/Users/{user_name}/IPEdits"
            if not os.path.exists(target_folder):
                os.mkdir(target_folder)
                break
            else:
                break
        else:
            fillchar.in_between("Enter a valid choice")
    os.chdir(image_folder[0])
    image_filters = selected_edits[0]
    image_enhancements = selected_edits[1]
    image_resize = selected_edits[2]
    num = 0
    edited_images = []
    img_extensions = []
    fillchar.sub_menu("Applying Edits...")
    if len(image_filters) != 0:
        num += 1
        edited_images = apply_filters(selected_images, image_filters, edited_images)
        fillchar.in_between(f"Filters were added to {len(selected_images)} images")

    if len(image_enhancements) != 0:
        num += 1
        if num == 2:
            last_edits = edited_images
        else:
            last_edits = selected_images
        edited_images = apply_enhancements(last_edits, image_enhancements, edited_images, num)
        fillchar.in_between(f"Enhancements were added to {len(selected_images)} images")
        if num == 2:
            edited_images = edited_images[len(selected_images):]
        num -= 1

    if len(image_resize) != 0:
        num += 1
        if num == 2:
            last_edits = edited_images
        else:
            last_edits = selected_images
        edited_images, img_size, img_size_flag = apply_size(last_edits, image_resize, edited_images, num)
        fillchar.in_between(f"{len(selected_images)} images were resized to {img_size} with {img_size_flag} property")
        if num == 2:
            edited_images = edited_images[len(selected_images):]
        num -= 1

    fillchar.in_between("All edits applied successfully")
    file_format = apply_format()

    for image in selected_images:
        img_extensions.append(str(image).split('.')[-1])
    num = 0

    for image in edited_images:
        img_name = selected_images[num]
        img_name = '.'.join(img_name.split('.')[:-1])
        if file_format == 'Default':
            extension = img_extensions[num]
            image.save(f"{target_folder}/{img_name}.{extension}")

        else:
            extension = file_format
            image.save(f"{target_folder}/{img_name}.{extension}")
        num += 1
    print(f"{fillchar.draw_line()}\nAll images were saved to target folder: {target_folder}")
    while True:
        user_choice = input(f"{fillchar.draw_line()}\nDo you want to open target folder?\n{fillchar.draw_line()}"
                            f"\nUSER(Y/N): ").lower()
        if user_choice == 'y':
            webbrowser.open(target_folder)
        elif user_choice == 'n':
            pass
        else:
            fillchar.in_between("Enter a valid choice")
            continue
        break


def apply_filters(selected_images, selected_filters, edited_images):
    print("Applying filters...")
    for image in selected_images:
        img = Image.open(image)
        for filters in selected_filters:
            img = img.filter(filters)
        edited_images.append(img)
    return edited_images


def apply_enhancements(last_edits, image_enhancements, edited_images, num):
    print("Applying Enhancements...")
    for image in last_edits[:len(last_edits)]:
        if num == 2:
            pass
        else:
            image = Image.open(image)
        for enhancement, val in image_enhancements.items():
            image = enhancement(image)
            image = image.enhance(val)
        edited_images.append(image)
    return edited_images


def apply_size(last_edits, image_resize, edited_images, num):
    img_size_flag = [x for x in image_resize.keys()][0]
    img_size = [x for x in image_resize.values()][0]
    img_width = int(img_size[0])
    img_height = int(img_size[1])
    img_size = (img_width, img_height)
    print("Applying Size...")
    for image in last_edits[:len(last_edits)]:
        if num == 2:
            pass
        else:
            image = Image.open(image)
        if img_size_flag == 'Thumbnail':
            image.thumbnail(img_size, Image.ANTIALIAS)
            edited_images.append(image)
        else:
            image = image.resize(img_size)
            edited_images.append(image)

    return edited_images, img_size, img_size_flag


def apply_format():
    file_format = ""
    while True:
        fillchar.sub_menu(" Image Format Selector ")
        user_choice = input(f"1. PNG\n2. JPEG\n3. JPG\n4. Default\n{fillchar.draw_line()}\nUSER:")
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
    return file_format


if __name__ == "__main__":
    apply_edits(image_folder="", selected_images=[], selected_edits=[])
