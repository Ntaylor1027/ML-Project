import random  # Used to seed the faker generator
import json
import time
from faker import Faker  # PII data generator
from faker.providers import person, phone_number, ssn, internet, address, credit_card
import numpy as np  # Used for random selection using weighted probabilites
import copy


def create_faker(seed):
    """
    Create and initialize a Faker instance.
    """
    fake = Faker()
    fake.seed(seed)
    # fake.add_provider(person)
    # fake.add_provider(phone_number)

    # List of function names to call for generating PII information.
    func_names = [
        'name', 'phone_number',
        'ssn', 'credit_card_number',
        'email']
    return (fake, func_names)


class CsvGenerator:
    #   Name: csvGenerator
    #
    #   Created By: Noah Taylor and Cole Bennett
    #
    #    Descriptions: csvGenerator is a class that defines the setup of the random csv including PII
    #
    #   Constructor Inputs:
    #       total_cols -> int: the total number of columns that will be in the CSV
    #       total_rows -> int: the total number of row entries that will be in the CSV
    #       total_pii -> int: Defines the total number of columns that will include PII
    #       csvName -> string: Name of csv to output to
    #
    #   Attributes:
    #       columnTags: List of generic labels to define columns
    #       csvName: output file name
    #       faker: fake data generator
    #
    #   Functions:
    #       generate_entry(columnTags): creates an entry row based on the columnTags
    #       outputCSV()
    #

    def __init__(self, total_cols, total_rows, total_pii, faker):
        self.total_cols = total_cols
        self.total_rows = total_rows
        self.total_pii = total_pii
        self.faker = faker[0]
        self.funcs = faker[1]
        self.create_column_tags()

    def create_column_tags(self):
        """
        Generate a random list of PII categories to choose from. Each category
        maps to a column in the CSV data.
        """
        tags = []
        pii_column_tags = self.funcs
        ceil_pii_probability = round(
            (self.total_pii / float(self.total_rows)), 2)
        filler_probability = 1 - ceil_pii_probability

        # Shuffle columns to randomize first pick for probability
        np.random.shuffle(pii_column_tags)

        # used to grab a subset of total fakers
        pii_avaliable = random.randrange(2, len(pii_column_tags)-1)
        # full list a pii column tags used for data
        full_pii_list = pii_column_tags[0:pii_avaliable]
        # keep track of removing entries to lower duplicate counts
        current_pii = copy.deepcopy(full_pii_list)

        # Loop decision making while keeping track of total
        total_entries = self.total_cols
        total_pii = self.total_pii
        total_filler = total_entries - total_pii
        while(total_entries != 0):
            if not current_pii:
                current_pii = copy.deepcopy(full_pii_list)

            if(total_pii == 0):
                # All pii entries have been placed
                tags.append('filler')

            elif(total_filler == 0):
                # Only room left to fill in PII entries
                choice = random.choice(current_pii)
                current_pii.remove(choice)
                tags.append(choice)

            else:
                # Random Descision
                entry_type = np.random.choice(['pii', 'filler'], 1, p=[
                    ceil_pii_probability, filler_probability])
                if(entry_type == 'pii'):
                    choice = random.choice(current_pii)
                    current_pii.remove(choice)
                    tags.append(choice)
                    total_pii -= 1
                else:
                    tags.append('filler')
                    total_filler -= 1

            total_entries -= 1
        self.column_tags = tags

    def add_pii_to_filler(self, filler):
        """
        Adds a random subset of pii to filler text
        """
        pii_to_add = random.sample(
            self.funcs, random.randint(1, len(self.funcs)-1))
        pii_added = []  # Keep track of pii entries to find positions
        entities = []
        filler = filler.split(" ")  # Convert to list
        for pii_tag in pii_to_add:
            pii_val = getattr(self.faker, pii_tag)()
            filler.insert(len(filler)-1, pii_val)  # Randomly insert pii
            pii_added.append((pii_tag, pii_val))

        filler = " ".join(filler)  # Convert filler back to string

        for pii in pii_added:
            start = filler.find(pii[1])
            end = start + (len(pii[1]) - 1)
            # Add position index and names of each pii added
            entities.append((start, end, pii[0]))
        return filler, entities

    def generate_value(self, col):
        """
        Generate a value (column) in the CSV data.
        """
        col_name = self.column_tags[col]
        entites = []  # if pii exists in a filler text
        if col_name == 'filler':
            # Generate a sentence that can contain PII.
            filler_sentence = self.faker.sentence(random.randrange(3, 20))
            # TODO: discuss if probability of pii in filler should be changed
            if(np.random.choice(['none', 'pii'], 1,
                                p=[.75, .25]) == 'pii'):  # Selecting if we will add PII
                filler_sentence, entites = self.add_pii_to_filler(
                    filler_sentence)
            return filler_sentence, entites
        return getattr(self.faker, col_name)(), []

    def generate_entry(self, create_metadata):
        """
        Generate an entry (line) in the CSV data.
        """
        entities = []
        pos = 0
        line = ""
        orig_last = 0  # Last index of the line
        for i in range(self.total_cols):
            val, fillerEntities = self.generate_value(i)
            val = val.replace("\n", " ").strip()  # remove new lines for now
            orig_last = len(line)
            line += val
            if i != self.total_cols - 1:
                line += ","
            entity_tag = self.column_tags[i].upper()
            if create_metadata and entity_tag != 'FILLER':
                entities.append((pos, pos + len(val), entity_tag))
                # print("%s '%s' %d-%d" %
                #      (entity_tag, line[pos:pos+len(val)], pos, pos+len(val)))
            elif create_metadata and entity_tag == 'FILLER':  # Filler might have pii in it
                for pii in fillerEntities:
                    entities.append(
                        (pii[0] + orig_last, pii[1] + orig_last + 1, pii[2].upper()))  # add the pii
                    # print("   > %s '%s' %d-%d" % (pii[2].upper(), line[pii[0] + orig_last:pii[1] + orig_last + 1],
                    #                              pii[0] + orig_last, pii[1] + orig_last + 1))
            pos += len(val)
            if i != self.total_cols - 1:
                pos += 1
        return (line, (line, {"entities": entities}))

    def generate_output(self, create_metadata):
        """
        Generate CSV data with PII information.
        """
        csvLines = [",".join(self.column_tags)]
        metaEntries = []
        for i in range(self.total_rows):
            line, line_meta = self.generate_entry(create_metadata)
            csvLines.append(line)
            if line_meta:
                metaEntries.append(line_meta)
        return (csvLines, metaEntries)

    def write(self, name, create_metadata):
        """
        Write the CSV data and JSON meta files.
        """
        start_time = time.time()
        print('Generating data')
        csv, meta = self.generate_output(create_metadata)
        self.print_duration(start_time)

        print('Writing CSV')
        start_time = time.time()
        f = open("%s.csv" % (name), "w")
        for line in csv:
            f.write(line + "\n")
        f.close()
        self.print_duration(start_time)

        if create_metadata:
            print('Writing meta JSON')
            start_time = time.time()
            f = open("%s-meta.json" % (name), "w")
            # Note: remove the indent argument to disable pretty printing
            # and save space for the meta file
            f.write(json.dumps(meta, indent=2))
            f.close()
            self.print_duration(start_time)

    @staticmethod
    def print_duration(start_time):
        elapsed_time = time.time() - start_time
        print("Took %s" % (time.strftime("%H:%M:%S", time.gmtime(elapsed_time))))
