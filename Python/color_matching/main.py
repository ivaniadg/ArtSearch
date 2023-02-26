import cm_utils as cm

# data = cm.process_folder("/home/mortirreke/Desktop/assets/")
data = cm.load_data()
#
results = cm.find_matches2("/home/mortirreke/Desktop/assets/duccio_madonna-and-child-on-a-throne-front-side-fragment-1311-10.jpg", data)

print(results)
