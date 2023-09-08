# This code is referenced from github repository https://github.com/realChrisHahn2/nl2spec

import LTL_parser
import server


def main():
    # Parse the command-line arguments using the LTL_parser module
    args = LTL_parser.parse_args()

    # Call the server to process the parsed arguments
    server_result = server.call_model(args)
    print(f"The final result is {server_result}")

    # Print the final translation with confidence score
    print("Final translation with confidence score:")
    print(server_result[0])

   # Write the final translation to a file
    # with open("final_translation.txt", "a") as file:
    #     file.write(server_result[0][0] + "\n")

    # Print sub-translations with confidence scores (excluding locked information)
    print("Sub-translations with confidence scores:")
    print(server_result[1][:-1])  # Remove the information whether a subtranslation is locked
    return


if __name__ == "__main__":
    main()
