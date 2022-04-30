import dpav
import pygame

clock = pygame.time.Clock()


def main():
    dimensions = (320, 240)
    buffer = dpav.VBuffer(dimensions)
    window = dpav.Window(buffer, 3.0)

    window.open()

    cga_scroll_text_x = 0
    cga_scroll_string = "Looky moving text...  Watch it go..."
    cga_scroll_spill = False

    vga_scroll_text_x = 0
    vga_scroll_string = "Big VGA letters!  The fidelity..."
    vga_scroll_spill = False

    rainbow_colors = [0xFF0000, 0xFF8800, 0x888800, 0x00FF00, 0x00FF88, 0x008888, 0x0088FF, 0x0000FF, 0x880088]


    while window.is_open():

        # Clear the buffer
        buffer.clear()

        # Create a font renderers
        cga_font = dpav.FontRenderer()
        vga_font = dpav.FontRenderer()

        vga_font.character_type = dpav.CHARACTER_ROM_TYPES[1]
        vga_font.character_rom = dpav.CHARACTER_ROM_VGA_8x16

        # Draw some text

        # Rainbow colors



        # Draw individual CGA characters
        cga_font.draw_string(buffer, "C", 152, 128, rainbow_colors, 0x112255)
        cga_font.draw_string(buffer, "G", 160, 128, rainbow_colors, 0x225511)
        cga_font.draw_string(buffer, "A", 168, 128, rainbow_colors, 0x551122)

        # Draw individual VGA characters
        vga_font.draw_string(buffer, "V", 152, 150, rainbow_colors, 0x113366)
        vga_font.draw_string(buffer, "G", 160, 150, rainbow_colors, 0x336611)
        vga_font.draw_string(buffer, "A", 168, 150, rainbow_colors, 0x661133)

        # Draw corner partial drawing characters for testing
        cga_font.draw_string(buffer, "X", -4, -4, 0xEE0000, 0x222222)
        cga_font.draw_string(buffer, "X", 316, -4, 0xEE0000, 0x222222)
        cga_font.draw_string(buffer, "X", -4, 236, 0xEE0000, 0x222222)
        cga_font.draw_string(buffer, "X", 316, 236, 0xEE0000, 0x222222)

        # Static Test String
        cga_font.draw_string(buffer, "Static Test String?!", 90, 100, 0x00EE00, 0x104410)
        cga_font.draw_string(buffer, "Static Test String?!", 90, 108, 0x00EE00, False)
        cga_font.draw_string(buffer, "Static Test String?!", 90, 116, False, 0x104410)

        # Draw Color Test Block
        cga_font.draw_string(buffer, "█", 20, 180, dpav.ClassicColors16.BLACK, False)
        cga_font.draw_string(buffer, "█", 28, 180, dpav.ClassicColors16.RED, False)
        cga_font.draw_string(buffer, "█", 36, 180, dpav.ClassicColors16.GREEN, False)
        cga_font.draw_string(buffer, "█", 44, 180, dpav.ClassicColors16.YELLOW, False)
        cga_font.draw_string(buffer, "█", 52, 180, dpav.ClassicColors16.BLUE, False)
        cga_font.draw_string(buffer, "█", 60, 180, dpav.ClassicColors16.MAGENTA, False)
        cga_font.draw_string(buffer, "█", 68, 180, dpav.ClassicColors16.CYAN, False)
        cga_font.draw_string(buffer, "█", 76, 180, dpav.ClassicColors16.WHITE, False)
        cga_font.draw_string(buffer, "█", 84, 180, dpav.ClassicColors16.BR_BLACK, False)
        cga_font.draw_string(buffer, "█", 92, 180, dpav.ClassicColors16.BR_RED, False)
        cga_font.draw_string(buffer, "█", 100, 180, dpav.ClassicColors16.BR_GREEN, False)
        cga_font.draw_string(buffer, "█", 108, 180, dpav.ClassicColors16.BR_YELLOW, False)
        cga_font.draw_string(buffer, "█", 116, 180, dpav.ClassicColors16.BR_BLUE, False)
        cga_font.draw_string(buffer, "█", 124, 180, dpav.ClassicColors16.BR_MAGENTA, False)
        cga_font.draw_string(buffer, "█", 130, 180, dpav.ClassicColors16.BR_CYAN, False)
        cga_font.draw_string(buffer, "█", 138, 180, dpav.ClassicColors16.BR_WHITE, False)

        # Scrolling Test String

        #
        # CGA Scrolling Text
        #
        # Check to see if the scrolling test has completely looped around
        if cga_scroll_text_x >= buffer.get_dimensions()[0]:
            cga_scroll_spill = False
            cga_scroll_text_x = 0

        if (cga_scroll_text_x + len(cga_scroll_string) * 8) >= buffer.get_dimensions()[0]:
            cga_scroll_spill = True

        # Draw the primary string
        cga_font.draw_string(buffer,
                             cga_scroll_string,
                             0 + cga_scroll_text_x,
                             10,
                             0x008844,
                             0x002200)

        # Draw the spill over string
        if cga_scroll_spill:
            cga_font.draw_string(buffer,
                                 cga_scroll_string,
                                 0 + cga_scroll_text_x - buffer.get_dimensions()[0],
                                 10,
                                 0x008844,
                                 0x002200)

        cga_scroll_text_x += 1

        #
        #  VGA Scrolling Text
        #
        # Check to see if the scrolling test has completely looped around
        if vga_scroll_text_x >= buffer.get_dimensions()[0]:
            vga_scroll_spill = False
            vga_scroll_text_x = 0

        if (vga_scroll_text_x + len(vga_scroll_string) * 8) >= buffer.get_dimensions()[0]:
            vga_scroll_spill = True

        # Draw the primary string
        vga_font.draw_string(buffer,
                              vga_scroll_string,
                              0 + vga_scroll_text_x,
                              200,
                              0x008844,
                              0x002200)

        # Draw the spill over string
        if vga_scroll_spill:
            vga_font.draw_string(buffer,
                                  vga_scroll_string,
                                  0 + vga_scroll_text_x - buffer.get_dimensions()[0],
                                  200,
                                  0x008844,
                                  0x002200)

        vga_scroll_text_x += 1

        #
        #  ASCII Box Draw
        #
        # Draw extended ASCII character ╔
        cga_font.draw_string(buffer, "╔", 50, 50, 0x1155EE, rainbow_colors)

        # Draw extended ASCII character ╚
        cga_font.draw_string(buffer, "╚", 50, 80, 0x1155EE, rainbow_colors)

        # Draw extended ASCII character ╗
        cga_font.draw_string(buffer, "╗", 200, 50, 0x1155EE, rainbow_colors)

        # Draw extended ASCII character ╝
        cga_font.draw_string(buffer, "╝", 200, 80, 0x1155EE, rainbow_colors)

        for x in range(58, 200, 8):
            # Draw extended ASCII character ═
            dpav.draw_8x8_character(buffer, dpav.CHARACTER_ROM_CGA_8x8[0xCD], x, 50, 0x1155EE, rainbow_colors)
            dpav.draw_8x8_character(buffer, dpav.CHARACTER_ROM_CGA_8x8[0xCD], x, 80, 0x1155EE, rainbow_colors)

        for y in range(58, 80, 8):
            # Draw extended ASCII character ═
            dpav.draw_8x8_character(buffer, dpav.CHARACTER_ROM_CGA_8x8[0xBA], 50, y, 0x1155EE, rainbow_colors)
            dpav.draw_8x8_character(buffer, dpav.CHARACTER_ROM_CGA_8x8[0xBA], 200, y, 0x1155EE, rainbow_colors)

        # Rotate the rainbow
        rainbow_colors.append(rainbow_colors.pop(0))

        # Update the window with the buffer
        window.update()

        # Wait about 15 ms
        clock.tick(15)


main()
