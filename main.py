import luigi
from luigi import Task, LocalTarget


class ProcessOrders(Task):
    def output(self):
        return LocalTarget('orders.csv')

    def run(self):
        with self.output().open('w') as f:
            print('May,100', file=f)
            print('May,170', file=f)
            print('June,89', file=f)
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


class SummarizeReport(Task):
    def requires(self):
        return GenerateReport()

    def output(self):
        return LocalTarget('summary.txt')

    def run(self):
        total = 0.0
        for line in self.input().open():
            month, amount = line.split(',')
            total += float(amount)
        with self.output().open('w') as f:
            f.write(str(total))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    luigi.run(['SummarizeReport'])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
