import unittest
import vmc.lattice as lattice

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from moviepy.video.io.bindings import mplfig_to_npimage
    import moviepy.editor as mpy
    duration = 2

    lattice = lattice.Square((3, 4), pbc=True)
    x1 = []
    y1 = []
    x2 = []
    y2 = []
    count = 0
    nodes = list(lattice.grid(nn=0))
    nearest = list(lattice.grid(nn=1))
    nextnearest = list(lattice.grid(nn=2))
    print(nodes, len(nodes))
    print(nearest, len(nearest))
    print(nextnearest, len(nextnearest))
    fig_mpl, ax = plt.subplots(1, figsize=(5, 5), facecolor='white')
    # ANIMATE WITH MOVIEPY (UPDATE THE CURVE FOR EACH t). MAKE A GIF.
    count = 0
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(-0.5, 3.5)
    plt.grid()

    lines = nextnearest

    def make_frame_mpl(t):
        global count
        if count < len(lines):
            a, b = lines[count]
            ax.plot([a[0], b[0]],
                    [a[1], b[1]], 'bo-')
            count += 1
        return mplfig_to_npimage(fig_mpl)  # RGB image of the figure

    animation = mpy.VideoClip(make_frame_mpl, duration=duration)
    # animation.write_gif("sinc_mpl.gif", fps=20)
    animation.write_videofile("my_animation.mp4", fps=24)
