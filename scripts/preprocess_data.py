from src.nombres_arg.data_processing import NameDataProcessor

def main():
    processor = NameDataProcessor()
    processor.run(save_intermediate=True)

if __name__ == "__main__":
    main()