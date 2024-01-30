## Generative AI for Humanity
# Introduction
Generative AI, such as Generative Adversarial Networks (GANs), refers to a technological approach that uses deep learning models to produce content that closely resembles human-generated content, such as images and phrases. This technology can generate responses to diverse and intricate prompts, including different languages, instructions, and inquiries [1]. In recent years, there have been notable breakthroughs in Generative AI. The progress in technology has resulted in significant enhancements in the capabilities of Generative AI, enabling it to generate content of exceptional realism, including artwork and photographs [2]. The images produced by Generative AI rely heavily on extensive datasets comprising human images, which leads to substantial privacy concerns. These privacy risks become even more pronounced when considering the potential outcomes of others exploiting these databases.  

Therefore, it has become essential to anonymize the datasets in ways that preserve their utility and privacy. We aimed to describe a unique identity disentanglement technique which constitutes an anonymization process achieved by modifying the gender of the input image within the latent space and pixel space. The solutions we offer are part of our framework, which is designed to: identify and manipulate identity-relevant information in a face to produce an anonymized face and maintain nonidentity-related features (such as hair, background, and pose) without compromising the naturalness of the face.  

Our methodology entails the integration of StyleGAN2 and Pix2PixHD, which guarantees the production of authentic content and the effective safeguarding of privacy. The proficiency of StyleGAN2 in generating synthetic data while preserving statistical traits by anonymizing serves as a valuable complement to Pix2PixHD 's capability to proactively translate AI-generated images into high-resolution, realistic representations. The generated output includes both an anonymized image and a numerical score indicating the extent of similarity between the anonymized image and the source image.  

To quantify this similarity, we employed the cosine similarity measure, a mathematical method that assesses the resemblance between two vectors based on the cosine of the angle between them [3]. This measure serves as a reliable indicator of the degree of likeness between the anonymized and source images. A higher cosine similarity score signifies a closer match, while a lower score indicates greater dissimilarity. This approach not only provides an anonymized image but also furnishes a quantitative measure, allowing for a nuanced evaluation of the effectiveness of the anonymization process in preserving key features from the source image. It also emphasizes the ethical obligations of transparency and responsible data handling, thereby paving the way for a future where technological advancements and privacy safeguards can coexist harmoniously. 

# GitHub Link
https://github.com/mcs192023/Final_Modal.git

# End User Guide
Our generative AI model can be accessed in Google Colab. It is built on Jupyter Notebook platform and provides free access to GPU resources. Without any hassle of setting up the environment, run our model using the following link: 

https://colab.research.google.com/drive/15RFBtXzo-lvKwMCkgh_0ZgeCASOPOgLE?usp=sharing 

# Refer to the final report pdf for more information 
