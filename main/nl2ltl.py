# MIT License
# 
# Copyright (c) 2023 Christoper Hahn
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
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
