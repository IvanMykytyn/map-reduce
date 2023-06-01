

if __name__ == '__main__':
    content = ''
    contentfull_lines = []
    with open('novel_test.txt', 'r') as file:
        content = file.read()

        lines = content.splitlines()
        for line in lines:
            if line:
                contentfull_lines.append(line)

        # print(len(contentfull_lines))
        # print(contentfull_lines)
        with open('novel_test.txt', 'w') as new_file:
            new_content = ''
            for new_line in contentfull_lines:
                new_content += new_line + '\n'

            new_file.write(new_content)

