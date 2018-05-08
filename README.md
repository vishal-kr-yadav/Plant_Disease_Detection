Reference : https://www.pyimagesearch.com/2014/12/01/complete-guide-building-image-search-engine-python-opencv/  
run on Python 2.7 and OpenCV 2.4.X.


It's manually tagging your images.  
search your collection of images using an another image?

Image search is not at all similar to text search you’re not using text as your query, you are instead using an image.
  
In general, there tend to be three types of image search engines: search by meta-data, search by example, and a hybrid approach of the two.


**Search by Meta-Data**
Searching by meta-data is only marginally different than your standard keyword-based search engines mentioned above. Search by meta-data systems rarely examine the contents of the image itself. Instead, they rely on textual clues such as (1) manual annotations and tagging performed by humans along with (2) automated contextual hints, such as the text that appears near the image on a webpage.

When a user performs a search on a search by meta-data system they provide a query, just like in a traditional text search engine, and then images that have similar tags or annotations are returned.
A great example of a Search by Meta-Data image search engine is Flickr.



**Search by Example**
Search by example systems, on the other hand, rely solely on the contents of the image — no keywords are assumed to be provided. The image is analyzed, quantified, and stored so that similar images are returned by the system during a search.


**Content-Based Image Retrieval (CBIR)**

Image search engines that quantify the contents of an image are called Content-Based Image Retrieval (CBIR) systems.
**A great example of a Search by Example system is TinEye.**
TinEye is actually a reverse image search engine where you provide a query image, and then TinEye returns near-identical matches of the same image, along with the webpage that the original image appeared on.



### Concepts:
When building an image search engine we will first have to index our dataset. Indexing a dataset is the process of quantifying our dataset by utilizing an image descriptor to extract features from each image.


An image descriptor defines the algorithm that we are utilizing to describe our image.

For example:

    The mean and standard deviation of each Red, Green, and Blue channel, respectively,
    The statistical moments of the image to characterize shape.
    The gradient magnitude and orientation to describe both shape and texture.
The important takeaway here is that the image descriptor governs how the image is quantified.
Features, on the other hand, are the output of an image descriptor. When you put an image into an image descriptor, you will get features out the other end.


In the most basic terms, features (or feature vectors) are just a list of numbers used to abstractly represent and quantify images.



Feature vectors can then be compared for similarity by using a distance metric or similarity function.



 Distance metrics and similarity functions take two feature vectors as inputs and then output a number that represents how “similar” the two feature vectors are.
 
 
 






