import dpav as dpp
import pygame

clock = pygame.time.Clock()


def main():
    dimensions = (320, 240)
    buffer = dpp.VBuffer(dimensions)
    window = dpp.Window(buffer, 3.0)

    window.open()

    cga_scroll_text_x = 0
    cga_scroll_string = "Looky moving text...  Watch it go..."
    cga_scroll_spill = False

    vga_scroll_text_x = 0
    vga_scroll_string = "Big VGA letters!  The fidelity..."
    vga_scroll_spill = False

    while window.is_open():

        # Clear the buffer
        buffer.clear()

        # Draw some text

        # Draw individual CGA characters
        dpp.draw_8x8_string(buffer, "C", 152, 120, 0xDDDDDD, 0x112255, dpp.CHARACTER_ROM_CGA_8x8)
        dpp.draw_8x8_string(buffer, "G", 160, 120, 0xDDDDDD, 0x225511, dpp.CHARACTER_ROM_CGA_8x8)
        dpp.draw_8x8_string(buffer, "A", 168, 120, 0xDDDDDD, 0x551122, dpp.CHARACTER_ROM_CGA_8x8)

        # Draw individual VGA characters
        dpp.draw_8x16_string(buffer, "V", 152, 150, 0xDDDDDD, 0x113366, dpp.CHARACTER_ROM_VGA_8x16)
        dpp.draw_8x16_string(buffer, "G", 160, 150, 0xDDDDDD, 0x336611, dpp.CHARACTER_ROM_VGA_8x16)
        dpp.draw_8x16_string(buffer, "A", 168, 150, 0xDDDDDD, 0x661133, dpp.CHARACTER_ROM_VGA_8x16)

        # Draw corner partial drawing characters for testing
        dpp.draw_8x8_string(buffer, "X", -4, -4, 0xEE0000, 0x222222, dpp.CHARACTER_ROM_CGA_8x8)
        dpp.draw_8x8_string(buffer, "X", 316, -4, 0xEE0000, 0x222222, dpp.CHARACTER_ROM_CGA_8x8)
        dpp.draw_8x8_string(buffer, "X", -4, 236, 0xEE0000, 0x222222, dpp.CHARACTER_ROM_CGA_8x8)
        dpp.draw_8x8_string(buffer, "X", 316, 236, 0xEE0000, 0x222222, dpp.CHARACTER_ROM_CGA_8x8)

        # Static Test String
        dpp.draw_8x8_string(buffer, "Static Test String?!", 90, 100, 0x00EE00, 0x104410, dpp.CHARACTER_ROM_CGA_8x8)

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
        dpp.draw_8x8_string(buffer,
                            cga_scroll_string,
                            0 + cga_scroll_text_x,
                            10,
                            0x008844,
                            0x002200,
                            dpp.CHARACTER_ROM_CGA_8x8)

        # Draw the spill over string
        if cga_scroll_spill:
            dpp.draw_8x8_string(buffer,
                                cga_scroll_string,
                                0 + cga_scroll_text_x - buffer.get_dimensions()[0],
                                10,
                                0x008844,
                                0x002200,
                                dpp.CHARACTER_ROM_CGA_8x8)

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
        dpp.draw_8x16_string(buffer,
                             vga_scroll_string,
                             0 + vga_scroll_text_x,
                             200,
                             0x008844,
                             0x002200,
                             dpp.CHARACTER_ROM_VGA_8x16)

        # Draw the spill over string
        if vga_scroll_spill:
            dpp.draw_8x16_string(buffer,
                                 vga_scroll_string,
                                 0 + vga_scroll_text_x - buffer.get_dimensions()[0],
                                 200,
                                 0x008844,
                                 0x002200,
                                 dpp.CHARACTER_ROM_VGA_8x16)

        vga_scroll_text_x += 1

        #
        #  ASCII Box Draw
        #
        # Draw extended ASCII character ╔
        dpp.draw_8x8_character(buffer, dpp.CHARACTER_ROM_CGA_8x8[0xC9], 50, 50, 0x1155EE, 0x102200)

        # Draw extended ASCII character ╚
        dpp.draw_8x8_character(buffer, dpp.CHARACTER_ROM_CGA_8x8[0xC8], 50, 80, 0x1155EE, 0x102200)

        # Draw extended ASCII character ╗
        dpp.draw_8x8_character(buffer, dpp.CHARACTER_ROM_CGA_8x8[0xBB], 200, 50, 0x1155EE, 0x102200)

        # Draw extended ASCII character ╝
        dpp.draw_8x8_character(buffer, dpp.CHARACTER_ROM_CGA_8x8[0xBC], 200, 80, 0x1155EE, 0x102200)

        for x in range(58, 200, 8):
            # Draw extended ASCII character ═
            dpp.draw_8x8_character(buffer, dpp.CHARACTER_ROM_CGA_8x8[0xCD], x, 50, 0x1155EE, 0x102200)
            dpp.draw_8x8_character(buffer, dpp.CHARACTER_ROM_CGA_8x8[0xCD], x, 80, 0x1155EE, 0x102200)

        for y in range(58, 80, 8):
            # Draw extended ASCII character ═
            dpp.draw_8x8_character(buffer, dpp.CHARACTER_ROM_CGA_8x8[0xBA], 50, y, 0x1155EE, 0x102200)
            dpp.draw_8x8_character(buffer, dpp.CHARACTER_ROM_CGA_8x8[0xBA], 200, y, 0x1155EE, 0x102200)

        # Update the window with the buffer
        window.update()

        # Wait about 15 ms
        clock.tick(15)


main()
