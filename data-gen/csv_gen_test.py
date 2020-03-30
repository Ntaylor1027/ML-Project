import unittest
from faker import Faker
from csv_gen import create_faker, CsvGenerator
import os


class CsvGeneratorTests(unittest.TestCase):
    def test_create_faker(self):
        testFake, testFuncNames = create_faker(0)

        testFakerType = type(testFake) == type(Faker())
        testFuncNamesTypes = len(list(filter(lambda name: isinstance(name, str), testFuncNames))) \
            == len(testFuncNames)

        self.assertTrue(testFakerType and testFuncNamesTypes,
                        "create_faker types are not correct")

    def test_CsvGenerator_init(self):
        testFake = create_faker(0)
        testCsvGenerator = CsvGenerator(5, 5, 3, testFake)
        self.assertEqual((testCsvGenerator.total_cols, testCsvGenerator.total_rows,
                          testCsvGenerator.total_pii, testCsvGenerator.faker, testCsvGenerator.funcs), (5, 5, 3, testFake[0], testFake[1]),
                         "Initial Values of CsvGenerator were not set properly")

    def test_CsvGenerator_add_pii_to_filler(self):
        # Description: Creates a CsvGenerator and adds pii to a random filler text
        # Pass if:
        #   The filler text after we remove pii from it remains the same as before it was added
        # Fails if:
        #   If no PII is added to the filler text we fail the test
        #   If we remove all the PII added and the text differs we fail the test
        testFake = create_faker(0)
        testCsvGenerator = CsvGenerator(10, 10, 4, testFake)
        filler = testCsvGenerator.faker.sentence(10)
        testSentence, testEntities = testCsvGenerator.add_pii_to_filler(
            filler)
        if len(testSentence) <= len(filler) and len(testEntities) == 0:
            self.fail("No Pii was added to the filler text")
        for entitie in testEntities:  # Set up PII for removal
            strToReplace = testSentence[entitie[0]:entitie[1]+1]
            testSentence = testSentence.replace(
                strToReplace, "@" * len(strToReplace))
        testSentence = testSentence.replace("@", "")
        fillerSplit = filler.split(" ")
        testSentenceSplit = testSentence.split(" ")
        while "" in testSentenceSplit:
            testSentenceSplit.remove("")
        self.assertEqual(len(fillerSplit), len(testSentenceSplit))

    # def test_CsvGenerator_generate_value(self):
        # Description: #TODO how will we validate a value generated besides existance

    def test_CsvGenerator_generate_entry(self):
        # Description: Tests that the number of entities is greater than or equal to the PII requested

        testFake = create_faker(0)
        testCsvGenerator = CsvGenerator(10, 10, 4, testFake)
        _, testLineMeta = testCsvGenerator.generate_entry(True)
        testLineMeta = testLineMeta[1:]  # Grab tuples of enties
        testLineMeta = testLineMeta[0]["entities"]
        self.assertGreaterEqual(len(
            testLineMeta), testCsvGenerator.total_pii, "Not enough PII was added to the entry")

    def test_CsvGenerator_generate_output(self):
        # Description: Tests that the number of rows and columns are correct in the CSV
        testFake = create_faker(0)
        testCsvGenerator = CsvGenerator(10, 10, 4, testFake)
        csv, meta = testCsvGenerator.generate_output(True)
        columns = csv[0]  # Column labels
        # The number of columns to test for in each row
        columnsNum = len(columns.split(","))
        csv = csv[1:]  # Generated rows
        for row in range(columnsNum):
            if(len(csv[row].split(",")) != columnsNum):
                self.fail(
                    f"Row {row} does not have the correct number of columns")

        self.assertEqual((columnsNum, len(csv), len(meta)), (testCsvGenerator.total_cols, testCsvGenerator.total_rows,
                                                             testCsvGenerator.total_rows), "The output files (csv and meta files) are not in the correct format (columns or rows).")

    def test_CsvGenerator_write(self):
        # Description: Tests that the CSV file and meta file were created and are not empty
        testFake = create_faker(0)
        testCsvGenerator = CsvGenerator(10, 10, 4, testFake)
        fileName = "testFile"
        testCsvGenerator.write(fileName, True)
        isEitherFileEmpty = os.stat(
            fileName+".csv").st_size == 0 or os.stat(fileName+"-meta.json").st_size == 0  # Validate each of the files are full
        self.assertIsNot(isEitherFileEmpty, True,
                         "One of the files (csv or meta) was not created or is empty")


if __name__ == '__main__':
    unittest.main()
