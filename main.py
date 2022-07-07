import luigi
from luigi import Task, LocalTarget


class ProcessOrders(Task):
    def output(self):
        return LocalTarget('orders.csv')

    def run(self):
        with self.output().open('w') as f:
            print('May,100', file=f)
            print('May,150', file=f)
            print('June,90', file=f)
            print('June,210', file=f)


class GenerateReport(Task):
    def requires(self):
        return ProcessOrders()

    def output(self):
        return LocalTarget('report.csv')

    def run(self):
        report = {}
        for line in self.input().open():
            month, amount = line.split(',')
            if month in report:
                report[month] += float(amount)
            else:
                report[month] = float(amount)
        with self.output().open('w') as out:
            for month in report:
                print(month + ',' + str(report[month]), file=out)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    luigi.run(['GenerateReport', '--local-scheduler'])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
