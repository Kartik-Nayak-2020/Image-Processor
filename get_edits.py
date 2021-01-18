from PIL import ImageFilter, ImageEnhance
import fillchar
from get_files import select_dir_files

image_filters, image_enhancements, image_resize = [], {}, {}
selected_edits = [image_filters, image_enhancements, image_resize]
display_selected = {'Filters': image_filters, "Enhancements": image_enhancements, "Size": image_resize}


def select_edits():
    while True:
        fillchar.sub_menu(' Edit Menu ')
        user_choice = input(f"1. Add filters\n2. Enhance Image\n3. Create thumbnail\n4. Show selection\n"
                            f"5. Continue with selection\n6. Reset values\n0. Select Image/DIR\n"
                            f"{fillchar.draw_line()}\nUSER: ").rstrip()
        print(fillchar.draw_line())
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
    fillchar.sub_menu(" Filter Selection Menu")
    if len(image_filters) != 10:
        filters = {1: ImageFilter.BLUR, 2: ImageFilter.CONTOUR, 3: ImageFilter.DETAIL,
                   4: ImageFilter.EDGE_ENHANCE, 5: ImageFilter.EDGE_ENHANCE_MORE,
                   6: ImageFilter.EMBOSS, 7: ImageFilter.FIND_EDGES, 8: ImageFilter.SHARPEN,
                   9: ImageFilter.SMOOTH, 10: ImageFilter.SMOOTH_MORE}
        filter_id = input(
            f"1. BLUR\n2. CONTOUR\n3. DETAIL\n4. EDGE_ENHANCE\n5. EDGE_ENHANCE_MORE\n6. EMBOSS\n"
            f"7. FIND_EDGES\n8. SHARPEN\n9. SMOOTH\n10. SMOOTH_MORE\n0. Edits Menu\n"
            f"Enter choice number separated by ' '(space)\n{fillchar.draw_line()}\nUSER: ").split(' ')
        print(fillchar.draw_line())
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
        fillchar.in_between(
            f"{image_filters[:3]}... is already selected\nReset values to change selection")


def select_enhancements():
    fillchar.sub_menu(" Enhancement Selection Menu ")
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
        fillchar.in_between(
            f"{[list(enhancement for enhancement in image_enhancements.keys())[:3]]}"
            f"... is already selected\nReset values to change selection")


def select_size():
    fillchar.sub_menu(" Image size selection Menu ")
    if len(image_resize) == 0:
        while True:
            user_choice = input(
                f"1. Thumbnail\n2. Custom size\n0. Edits Menu\n{fillchar.draw_line()}\nUSER:")
            if user_choice == '0':
                break

            elif user_choice == '1':
                img_size_flag = "Thumbnail"

            elif user_choice == '2':
                img_size_flag = "Custom"

            else:
                fillchar.in_between("Enter a valid option")
                continue

            img_size = input(
                "Enter size in pixels (format: 550 400): ").split(' ')

            if len(img_size) == 2:
                image_resize[img_size_flag] = img_size
                print(
                    f"Selected image size: {img_size}\nConversion type:{img_size_flag}")

            else:
                fillchar.in_between("Enter size in correct format!")
                continue

            break

    else:
        fillchar.in_between(
            f"Already [{[img_size for img_size in list(image_resize.values())[0]]}] size with "
            f"{[img_size_flag for img_size_flag in list(image_resize.keys())[0]]}\
             property is assigned\nReset values to assign new value")


def show_selection():
    fillchar.sub_menu(" Selected Edits ")
    for edit_name, edit in display_selected.items():
        print(f"{edit_name} : {edit}")


def reset_values():
    num = 0
    for edits in selected_edits:
        if len(edits) == 0:
            num += 1
    if num != 3:
        while True:
            fillchar.sub_menu(" Reset Menu ")
            user_choice = input(
                f"1. All values\n2. Specific Values\n0. Edits Menu\n{fillchar.draw_line()}\nUSER:")
            if user_choice == '0':
                break

            elif user_choice == '1':
                for edit in selected_edits:
                    edit.clear()
                fillchar.in_between("All values have been reset")

            elif user_choice == '2':
                while True:
                    user_choice = input(f"{fillchar.draw_line()}\n1. Filters\n2. Enhancements\n3. Size\n0. Reset Menu\
                    \n{fillchar.draw_line()}\nUSER:").split(' ')
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
                        fillchar.in_between("Selected Values have been reset")
                    break
                continue

            else:
                print("Enter a valid choice")
                continue
            break
    else:
        print("No values are currently selected to remove!")


if __name__ == "__main__":
    select_edits()
