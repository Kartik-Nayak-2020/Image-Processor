from PIL import Image, ImageFilter, ImageEnhance
import os
from tkinter import Tk, filedialog
import webbrowser

image_extensions = ('.png', '.jpg', 'jfif', 'jpeg')
selected_images, image_folder_path = [], []
image_filters, image_enhancements, image_resize = [], {}, {}
selected_edits = [image_filters, image_enhancements, image_resize]
display_selected = {'Filters': image_filters,
                    "Enhancements": image_enhancements, "Size": image_resize}


def select_files_menu():
    '''Option to continue with cuurent DIR selection or select new DIR for source images'''
    while True:
        if not len(selected_images) == 0:
            if len(selected_images) > 3:
                ch = "..."
            else:
                ch = ""
            while True:
                print(
                    f"{draw_line()}\nSelected DIR: {image_folder_path}\nSelected Images: [{len(selected_images)}] => "
                    f"{[x for x in selected_images][:3]}{ch}\n{draw_line()}")
                user_choice = input(
                    f"1. Change DIR/Image selection\n2. Continue with the selection\n{draw_line()}\nUSER:")
                if user_choice == '1':
                    selected_images.clear()
                    image_folder_path.clear()
                    select_dir_files()
                elif user_choice == '2':
                    return image_folder_path, selected_images
                else:
                    print("Enter a valid option")
                    continue
                break
        else:
            select_dir_files()


def select_dir_files():
    '''Select source DIR of images'''
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    main_menu(" Image Processor v1.1.0 ")
    while True:
        user_choice = input(
            f"1. Select directory\n2. Select image\n3. Exit\n{draw_line()}\nUSER:")
        if user_choice == '1':
            image_folder = filedialog.askdirectory()
            if image_folder:
                for item in os.listdir(image_folder):
                    if item.endswith(image_extensions):
                        selected_images.append(item)
            else:
                in_between("Directory opening terminated by user")
                continue

        elif user_choice == '2':
            image_selection = list(filedialog.askopenfilenames(
                filetypes=[("All Files", ".*")]))
            if image_selection:
                image_selection_path = image_selection[0]
                image_folder = '/'.join(image_selection_path.split('/')[:-1:])
                for image in image_selection:
                    image = image.split('/')[-1::]
                    selected_images.extend(
                        [x for x in image if str(x).endswith(image_extensions)])
            else:
                in_between("No files were selected")
                continue

        elif user_choice == '3':
            print("Application terminated by USER")
            exit()

        else:
            in_between("Enter a valid choice!")

        if len(selected_images) != 0:
            image_folder_path.append(image_folder)
            break
        break

    if len(selected_images) == 0:
        in_between("Directory doesn't contain any images")
        select_dir_files()


def select_edits():
    '''Edits menu to select between no of edit including adding filters, resizing images'''
    while True:
        sub_menu(' Edit Menu ')
        user_choice = input(f"1. Add filters\n2. Enhance Image\n3. Create thumbnail\n4. Show selection\n"
                            f"5. Continue with selection\n6. Reset values\n0. Select Image/DIR\n"
                            f"{draw_line()}\nUSER: ").rstrip()
        print(draw_line())
        if user_choice == '0':
            select_dir_files()

        elif user_choice == '1':
            select_filters()

        elif user_choice == '2':
            select_enhancements()

        elif user_choice == '3':
            select_size()

        elif user_choice == '4':
            show_selection()

        elif user_choice == '5':
            break

        elif user_choice == '6':
            reset_values()

        else:
            print("Enter a valid option!")

    if len(image_filters) == len(image_enhancements) == len(image_resize) == 0:
        print("No edits are currently selected\nSelect any to continue...")
        select_edits()

    else:
        return selected_edits


def select_filters():
    '''Select certain filters to images'''
    sub_menu(" Filter Selection Menu")
    if len(image_filters) != 10:
        filters = {1: ImageFilter.BLUR, 2: ImageFilter.CONTOUR, 3: ImageFilter.DETAIL,
                   4: ImageFilter.EDGE_ENHANCE, 5: ImageFilter.EDGE_ENHANCE_MORE,
                   6: ImageFilter.EMBOSS, 7: ImageFilter.FIND_EDGES, 8: ImageFilter.SHARPEN,
                   9: ImageFilter.SMOOTH, 10: ImageFilter.SMOOTH_MORE}
        filter_id = input(
            f"1. BLUR\n2. CONTOUR\n3. DETAIL\n4. EDGE_ENHANCE\n5. EDGE_ENHANCE_MORE\n6. EMBOSS\n"
            f"7. FIND_EDGES\n8. SHARPEN\n9. SMOOTH\n10. SMOOTH_MORE\n0. Edits Menu\n"
            f"Enter choice number separated by ' '(space)\n{draw_line()}\nUSER: ").split(' ')
        print(draw_line())
        for x in filter_id:
            if len(filter_id) == 1 and x == '0':
                break
            else:
                try:
                    x = int(x)
                    if 0 < x <= 10:
                        for num, img_filter in filters.items():
                            if img_filter not in image_filters:
                                if num == x:
                                    image_filters.append(img_filter)
                except:
                    continue

    else:
        in_between(
            f"{image_filters[:3]}... is already selected\nReset values to change selection")


def select_enhancements():
    '''Select certain enhancements to images'''
    sub_menu(" Enhancement Selection Menu ")
    if len(image_enhancements) != 4:
        enhancements = {1: ImageEnhance.Color, 2: ImageEnhance.Contrast,
                        3: ImageEnhance.Brightness, 4: ImageEnhance.Sharpness}
        enhancement_id = input(
            f"1. Color\n2. Contrast\n3. Brightness\n4. Sharpness\n0. Edits menu\n{'-' * 90}\nUSER: ").split(' ')

        for x in enhancement_id:
            if len(enhancement_id) == 1 and x == '0':
                break
            else:
                try:
                    x = int(x)
                    if 0 < x <= 4:
                        for num, img_enhancement in enhancements.items():
                            if img_enhancement not in image_enhancements:
                                if num == x:
                                    while True:
                                        value = input(
                                            f"Enter enhancement value for {str(img_enhancement).split('.')[2][:-2]}: ")
                                        try:
                                            value = float(value)
                                            if 0 <= value <= 4:
                                                image_enhancements[img_enhancement] = value
                                                break
                                            else:
                                                print(
                                                    "Enter a value between 0-4")
                                        except:
                                            print("Enter a valid value")
                                else:
                                    continue
                except:
                    continue

    else:
        in_between(
            f"{[list(enhancement for enhancement in image_enhancements.keys())[:3]]}"
            f"... is already selected\nReset values to change selection")


def select_size():
    '''Select certain size for images'''
    sub_menu(" Image size selection Menu ")
    if len(image_resize) == 0:
        while True:
            user_choice = input(
                f"1. Thumbnail\n2. Custom size\n0. Edits Menu\n{draw_line()}\nUSER:")
            if user_choice == '0':
                break

            elif user_choice == '1':
                img_size_flag = "Thumbnail"

            elif user_choice == '2':
                img_size_flag = "Custom"

            else:
                in_between("Enter a valid option")
                continue

            img_size = input(
                "Enter size in pixels (format: 550 400): ").split(' ')

            if len(img_size) == 2:
                image_resize[img_size_flag] = img_size
                print(
                    f"Selected image size: {img_size}\nConversion type:{img_size_flag}")

            else:
                in_between("Enter size in correct format!")
                continue

            break

    else:
        in_between(
            f"Already [{[img_size for img_size in list(image_resize.values())[0]]}] size with "
            f"{[img_size_flag for img_size_flag in list(image_resize.keys())[0]]}\
             property is assigned\nReset values to assign new value")


def show_selection():
    '''Show all selected edits'''
    sub_menu(" Selected Edits ")
    for edit_name, edit in display_selected.items():
        print(f"{edit_name} : {edit}")


def reset_values():
    '''Reset all selected edits or indivisual edits'''
    num = 0
    for edits in selected_edits:
        if len(edits) == 0:
            num += 1
    if num != 3:
        while True:
            sub_menu(" Reset Menu ")
            user_choice = input(
                f"1. All values\n2. Specific Values\n0. Edits Menu\n{draw_line()}\nUSER:")
            if user_choice == '0':
                break

            elif user_choice == '1':
                for edit in selected_edits:
                    edit.clear()
                in_between("All values have been reset")

            elif user_choice == '2':
                while True:
                    user_choice = input(f"{draw_line()}\n1. Filters\n2. Enhancements\n3. Size\n0. Reset Menu\
                    \n{draw_line()}\nUSER:").split(' ')
                    for x in user_choice:
                        if len(user_choice) == 1 and x == '0':
                            break
                        else:
                            try:
                                x = int(x)
                                if x == 1:
                                    selected_edits[0].clear()
                                elif x == 2:
                                    selected_edits[1].clear()
                                elif x == 3:
                                    selected_edits[2].clear()
                            except:
                                continue
                    if user_choice != list('0'):
                        print(f"{draw_line()}\nSelected Values have been reset")
                    break
                continue

            else:
                print("Enter a valid choice")
                continue
            break
    else:
        print("No values are currently selected to remove!")


def main_menu(string="="):
    '''Custom fillchar'''
    print(str(string).center(120, "="))


def sub_menu(string="-"):
    '''Custom fillchar'''
    print(str(string).center(120, "-"))


def draw_line(string="-"):
    '''Custom fillchar'''
    return string * 120


def in_between(msg, string='-'):
    '''Custom fillchar'''
    print(f"{string * 120}\n{msg}\n{string * 120}")


def get_username():
    '''Get user name from current system'''
    for user, name in os.environ.items():
        if user == "USERNAME":
            return name


def apply_edits(image_folder, selected_images, selected_edits):
    '''Select target folder to save images and apply all selected edits to selected images'''
    user_name = get_username()
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    while True:
        main_menu(" Apply Edits Menu ")
        user_choice = input(
            f"1. Select DIR to save images\n2. Continue with default DIR (User)\n{draw_line()}\nUSER:")
        if user_choice == '1':
            target_folder = filedialog.askdirectory()
            if target_folder:
                print(f"All edited images will be saved to {target_folder}")
                print("Target inside if", target_folder)
                break
        elif user_choice == '2':
            target_folder = f"C:/Users/{user_name}/IPEdits"
            if not os.path.exists(target_folder):
                os.mkdir(f"C:/Users/{user_name}/IPEdits")
                break
            else:
                break
        else:
            in_between("Enter a valid choice")
    os.chdir(image_folder[0])
    image_filters = selected_edits[0]
    image_enhancements = selected_edits[1]
    image_resize = selected_edits[2]
    num = 0
    edited_images = []
    img_extensions = []
    sub_menu("Applying Edits...")
    if len(image_filters) != 0:
        num += 1
        edited_images = apply_filters(
            selected_images, image_filters, edited_images)
        in_between(f"Filters were added to {len(selected_images)} images")

    if len(image_enhancements) != 0:
        num += 1
        if num == 2:
            last_edits = edited_images
        else:
            last_edits = selected_images
        edited_images = apply_enhancements(
            last_edits, image_enhancements, edited_images, num)
        in_between(f"Enhancements were added to {len(selected_images)} images")
        if num == 2:
            edited_images = edited_images[len(selected_images):]
        num -= 1

    if len(image_resize) != 0:
        num += 1
        if num == 2:
            last_edits = edited_images
        else:
            last_edits = selected_images
        edited_images, img_size, img_size_flag = apply_size(
            last_edits, image_resize, edited_images, num)
        in_between(
            f"{len(selected_images)} images were resized to {img_size} with {img_size_flag} property")
        if num == 2:
            edited_images = edited_images[len(selected_images):]
        num -= 1

    in_between("All edits applied successfully")
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
    print(f"{draw_line()}\nAll images were saved to target folder: {target_folder}")
    while True:
        user_choice = input(f"{draw_line()}\nDo you want to open target folder?\n{draw_line()}"
                            f"\nUSER(Y/N): ").lower()
        if user_choice == 'y':
            webbrowser.open(target_folder)
        elif user_choice == 'n':
            pass
        else:
            in_between("Enter a valid choice")
            continue
        break


def apply_filters(selected_images, selected_filters, edited_images):
    '''Apply selected filters to the selected images'''
    print("Applying filters...")
    for image in selected_images:
        img = Image.open(image)
        for filters in selected_filters:
            img = img.filter(filters)
        edited_images.append(img)
    return edited_images


def apply_enhancements(last_edits, image_enhancements, edited_images, num):
    '''Apply selected enhancements to the selected images'''
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
    '''Apply selected size to the selected images'''
    print("Applying size...")
    img_size_flag = [x for x in image_resize.keys()][0]
    img_size = [x for x in image_resize.values()][0]
    img_width = int(img_size[0])
    img_height = int(img_size[1])
    img_size = (img_width, img_height)
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
    '''Change Image format or keep it's default format while saving edited image'''
    file_format = ""
    while True:
        sub_menu(" Image Format Selector ")
        user_choice = input(
            f"1. PNG\n2. JPEG\n3. JPG\n4. Default\n{draw_line()}\nUSER:")
        if user_choice == '1':
            file_format = "png"
        elif user_choice == '2':
            file_format = "jpeg"
        elif user_choice == '3':
            file_format = "jpg"
        elif user_choice == '4':
            file_format = 'Default'
        else:
            in_between("Enter a valid choice!")
            continue
        break
    return file_format


if __name__ == "__main__":
    image_folder, selected_images = select_files_menu()
    finalized_edit_selection = select_edits()
    apply_edits(image_folder, selected_images, finalized_edit_selection)
