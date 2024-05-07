## Project Description:
Large language models have shown great positive impact across different domains. OpenAI being on the top with its closed source models creates a concern regarding data privacy. 
While other open source models such as Mistral, Llama, etc also have shown great performance in terms of benchmarking task. But using these open source models directly to edge cases doesn't produce great results. 
And techniques like Retrieval Augmentation Generation (RAG) have been generated. 

While, in this work we wanted to further explore by finetuning the Mistral 7B model using PEFT techniques such as LoRA. Doing this helps us to overcome the resource constraints. Futher after finetuning, we also wanted to test the model
in the RAG system. 

## Dataset Preparation:
During the phase, dataset preparation was one of the challenging task. We scraped textual contents from websites such as Food and Drug Administrations (FDA), Centers for Disease Control and Prevention (CSC) and also collected academic papers from PubMed. Once the raw textual data was collected, we created 18052 question and answer pairs utilizing Llama 2 model. To verify the generated data we manual inspected samples of data.


## Finetuning Mistral 7B model.

- GGUF weights can be downloaded from the here (https://drive.google.com/file/d/1Je72nQXO3xpq93iA6unJQcd-hHF4iELG/view?usp=drive_link)
