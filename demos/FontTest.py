import dpav as dpp
import pygame

clock = pygame.time.Clock()

def main():
    dimensions = (320, 240)
    buffer = dpp.VBuffer(dimensions)
    window = dpp.Window(buffer, 3.0)

    window.open()

    scrollTextCurrentX = 0
    stringToScroll = "Looky moving text...  Watch it go..."
    spillOverString = False


    while window.is_open():
        #Clear the buffer
        buffer.clear()

        # Draw some text

        # Draw individual characters
        dpp.font_draw_8x8_character(buffer, "C", 152, 120, 0xDDDDDD, 0x112255, dpp.CHARACTER_ROM_CGA_8x8)
        dpp.font_draw_8x8_character(buffer, "G", 160, 120, 0xDDDDDD, 0x225511, dpp.CHARACTER_ROM_CGA_8x8)
        dpp.font_draw_8x8_character(buffer, "A", 168, 120, 0xDDDDDD, 0x551122, dpp.CHARACTER_ROM_CGA_8x8)

        # Draw corner partial drawing characters for testing
        dpp.font_draw_8x8_character(buffer, "X", -4, -4, 0xEE0000, 0x222222, dpp.CHARACTER_ROM_CGA_8x8)
        dpp.font_draw_8x8_character(buffer, "X",  316, -4, 0xEE0000, 0x222222, dpp.CHARACTER_ROM_CGA_8x8)
        dpp.font_draw_8x8_character(buffer, "X", -4, 236, 0xEE0000, 0x222222, dpp.CHARACTER_ROM_CGA_8x8)
        dpp.font_draw_8x8_character(buffer, "X", 316, 236, 0xEE0000, 0x222222, dpp.CHARACTER_ROM_CGA_8x8)

        # Static Test String
        dpp.font_draw_8x8_string(buffer, "Static Test String?!", 90, 100, 0x00EE00, 0x104410, dpp.CHARACTER_ROM_CGA_8x8)

        # Scrolling Test String

        # Check to see if the scrolling test has completely looped around
        if scrollTextCurrentX >= buffer.get_dimensions()[0]:
            spillOverString = False
            scrollTextCurrentX = 0

        if (scrollTextCurrentX + len(stringToScroll)* 8) >= buffer.get_dimensions()[0]:
            spillOverString = True

        # Draw the primary string
        dpp.font_draw_8x8_string(buffer, stringToScroll, 0 + scrollTextCurrentX, 10, 0x008844, 0x002200, dpp.CHARACTER_ROM_CGA_8x8)

        # Draw the spill over string
        if (spillOverString):
            dpp.font_draw_8x8_string(buffer, stringToScroll, 0 + scrollTextCurrentX - buffer.get_dimensions()[0], 10, 0x008844, 0x002200, dpp.CHARACTER_ROM_CGA_8x8)


        scrollTextCurrentX += 1





        # Update the window with the buffer
        window.update()

        # Wait about 15 ms
        clock.tick(15)


main()


