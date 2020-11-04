import multiprocessing
import glob
import concurrent.futures
import os
import gzip

demo_path = "./demos"  # use this to set where all of your tar.gz demos are.
output_path = "./output"
amount_of_demos_found = len(glob.glob1(demo_path, "*.gz"))
demo_files = []


def extract_file(input_file, timeout):
    x = (demo_path) + "/" + (input_file)  # create the input file string.
    # open the input file string and open it with gzip output as bytes.
    f = gzip.open((x), 'rb')
    with open(os.path.join(output_path, input_file), 'wb') as temp_file:
        # read the byte stream coming out of the decompression and start writing it to new file.
        temp_file.write(f.read())
        f.close()  # we can close the decompression streaming now.
        temp_file.close()  # close the new file

    # take the file as we know it so /demos/*INPUTFILENAME*
    rename_value1 = (output_path) + ("/") + (input_file)
    rename_value2 = (output_path) + ("/") + (input_file) + \
        (".dem")  # Do the same thing but add .dem on the end
    # now preform the rename operation.
    os.rename(rename_value1, rename_value2)
    return ("done")  # boss man we are done here now!


print("Welcome")
print("You have " + str((multiprocessing.cpu_count())) + " cores we can use!")
input("Press Enter to continue...")

if amount_of_demos_found <= 0:
    print("Error we could not find any demos please check you have some .gz files!")
    exit()

print("I have found " + str((amount_of_demos_found)) + " demos")
demo_files = os.listdir(demo_path)
print(demo_files)

print("creating " + str((multiprocessing.cpu_count())) + " Workers")

with concurrent.futures.ThreadPoolExecutor(max_workers=(multiprocessing.cpu_count())) as executor:
    # Start the load operations and mark each future with its demo
    tar_to_demo = {executor.submit(
        extract_file, input_file, 60): input_file for input_file in demo_files}
    for future in concurrent.futures.as_completed(tar_to_demo):
        demo = tar_to_demo[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (demo, exc))
        else:
            print((demo) + (" : ") + (data))
