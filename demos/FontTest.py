import dpav as dpp
import pygame

clock = pygame.time.Clock()

def main():
    dimensions = (320, 240)
    buffer = dpp.VBuffer(dimensions)
    window = dpp.Window(buffer, 3.0)

    window.open()

    CGAscrollTextCurrentX = 0
    CGAstringToScroll = "Looky moving text...  Watch it go..."
    CGAspillOverString = False

    VGAscrollTextCurrentX = 0
    VGAstringToScroll = "Big VGA letters!  The fidelity..."
    VGAspillOverString = False


    while window.is_open():
        #Clear the buffer
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
        if CGAscrollTextCurrentX >= buffer.get_dimensions()[0]:
            CGAspillOverString = False
            CGAscrollTextCurrentX = 0

        if (CGAscrollTextCurrentX + len(CGAstringToScroll)* 8) >= buffer.get_dimensions()[0]:
            CGAspillOverString = True

        # Draw the primary string
        dpp.draw_8x8_string(buffer, CGAstringToScroll, 0 + CGAscrollTextCurrentX, 10, 0x008844, 0x002200, dpp.CHARACTER_ROM_CGA_8x8)

        # Draw the spill over string
        if (CGAspillOverString):
            dpp.draw_8x8_string(buffer, CGAstringToScroll, 0 + CGAscrollTextCurrentX - buffer.get_dimensions()[0], 10, 0x008844, 0x002200, dpp.CHARACTER_ROM_CGA_8x8)

        CGAscrollTextCurrentX += 1


        #
        #  VGA Scrolling Text
        #
        # Check to see if the scrolling test has completely looped around
        if VGAscrollTextCurrentX >= buffer.get_dimensions()[0]:
            VGAspillOverString = False
            VGAscrollTextCurrentX = 0

        if (VGAscrollTextCurrentX + len(VGAstringToScroll) * 8) >= buffer.get_dimensions()[0]:
            VGAspillOverString = True

        # Draw the primary string
        dpp.draw_8x16_string(buffer, VGAstringToScroll, 0 + VGAscrollTextCurrentX, 200, 0x008844, 0x002200, dpp.CHARACTER_ROM_VGA_8x16)

        # Draw the spill over string
        if (VGAspillOverString):
            dpp.draw_8x16_string(buffer, VGAstringToScroll, 0 + VGAscrollTextCurrentX - buffer.get_dimensions()[0], 200, 0x008844, 0x002200, dpp.CHARACTER_ROM_VGA_8x16)

        VGAscrollTextCurrentX += 1


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

        for x in range(58,200,8):
            # Draw extended ASCII character ═
            dpp.draw_8x8_character(buffer, dpp.CHARACTER_ROM_CGA_8x8[0xCD], x, 50, 0x1155EE, 0x102200)
            dpp.draw_8x8_character(buffer, dpp.CHARACTER_ROM_CGA_8x8[0xCD], x, 80, 0x1155EE, 0x102200)

        for y in range(58,80,8):
            # Draw extended ASCII character ═
            dpp.draw_8x8_character(buffer, dpp.CHARACTER_ROM_CGA_8x8[0xBA], 50, y, 0x1155EE, 0x102200)
            dpp.draw_8x8_character(buffer, dpp.CHARACTER_ROM_CGA_8x8[0xBA], 200, y, 0x1155EE, 0x102200)




        # Update the window with the buffer
        window.update()

        # Wait about 15 ms
        clock.tick(15)


main()


