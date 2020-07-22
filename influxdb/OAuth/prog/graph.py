import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from prog.db import Database, DBRequest

if __name__ == "__main__":
    Database.set_db('localhost', 'prr')
    DBRequest.set_mes('msn')
    fields = {}
    time = {}

    def animate(i):
        tm = DBRequest.get_params()
        if len(tm) == 0:
            return

        for a in fields:
            fields[a].clear()
            time[a].clear()

        for a in tm:
            timen = a.pop("time")
            for b in a:
                if a[b] is None:
                    continue
                if fields.get(b, None) is None:
                    time[b] = []
                    fields[b] = []
                fields[b].append(a[b])
                time[b].append(timen)
        plt.cla()
        for b in fields:
            plt.plot(time[b], fields[b], label=b)
        plt.tight_layout()
        plt.legend(loc='lower right')


    ani = FuncAnimation(plt.gcf(), animate, interval=500)
    plt.tight_layout()
    plt.show()
