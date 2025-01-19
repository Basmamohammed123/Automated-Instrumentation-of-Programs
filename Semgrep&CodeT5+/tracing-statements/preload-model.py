from transformers import AutoModel, AutoTokenizer

def preload_model_and_tokenizer():
    checkpoint = "Salesforce/codet5p-220m-bimodal"
    print("Starting the preloading process...")

    print("Downloading and caching the tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(checkpoint, trust_remote_code=True)
    print("Tokenizer cached successfully.")

    print("Downloading and caching the model...")
    model = AutoModel.from_pretrained(checkpoint, trust_remote_code=True)
    print("Model cached successfully!")

if __name__ == "__main__":
    print("Executing preload-model script...")
    preload_model_and_tokenizer()
    print("Preloading complete.")
