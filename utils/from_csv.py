import csv


class CSVWriter:
    """Create file.csv

    csv_writer = CSVWriter("file.csv")
    #### first created headers column\n
    csv_writer.write_row("name,age,city,count")\n
    csv_writer.write_row("Alice,30,New York,34")\n
    csv_writer.write_row("Bob,25,Los Angeles,23")\n
    return file.csv
    """

    def __init__(self, filename):
        self.filename = filename
        self.open_file()

    def open_file(self):
        self.file = open(self.filename, "w", newline="", encoding="utf-8")
        self.writer = csv.writer(self.file)
        self.header_written = False

    def write_row(self, row):
        if isinstance(row, str):
            row = row.split(",")
        if not self.header_written:
            self.writer.writerow(row)
            self.header_written = True
        else:
            self.writer.writerow(row)

    def close(self):
        self.file.close()

    def __del__(self):
        self.close()


if __name__ == "__main__":
    csv_writer = CSVWriter("test.csv")
    # Сначала запись заголовков
    csv_writer.write_row("name,age,city,count")
    csv_writer.write_row("Alice,30,New York,34")
    csv_writer.write_row("Bob,25,Los Angeles,23")