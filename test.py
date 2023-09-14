import matplotlib.pyplot as plt
if __name__ == "__main__":
    cmap = ['Crimson', 'Orchid', 'Magenta', 'Blue', 'DodgerBlue', 'DarkTurquoise',
            'Green', 'LimeGreen', 'YellowGreen','Yellow', 'Gold', 'Orange',
            'LightSalmon', 'DimGray']
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, aspect='equal')
    ax1.add_patch(
        plt.Rectangle(
            (1, 2),  # (x,y)矩形左下角
            3,  # width长
            4,  # height宽
            color=cmap[13],
            alpha=0.5
        )
    )
    plt.xlim(-1, 6)
    plt.ylim(1, 7)
    plt.show()
    fig1.savefig('rect1.png', dpi=90, bbox_inches='tight')
