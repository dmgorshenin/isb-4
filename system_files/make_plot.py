import matplotlib.pyplot as plt
import logging


logger = logging.getLogger()
logger.setLevel('INFO')


def make_plot(stats: set) -> plt:
    """Creates a time histogram of the number of cores

    Args:
        stats (set): Statistic

    Returns:
        plt: Image of histogram
    """
    x = stats.keys()
    y = stats.values()
    figure = plt.figure(figsize=(30, 5))
    plt.xlabel('Количество ядер')
    plt.ylabel('Время выполнения (сек)')
    plt.title('Гистограмма времени выполнения от количества ядер')
    plt.bar(x, y, color="orange", width=0.1)
    plt.show()
    logging.info('The image has been successfully built.')
    return figure
