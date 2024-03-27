STATUS_REMOVED = [
    {
        "sha": "1234",
        "filename": "some/file.somefile",
        "status": "removed",
        "additions": 0,
        "deletions": 100,
        "changes": 100,
        "blob_url": "https://example.com",
        "raw_url": "https://example.com",
        "contents_url": "https://example.com",
        "patch": ""
    },
]

STATUS_MODIFIED = [
    {
        "sha": "ceb55617e5c64117a9c02d8f95a001101d5d9210",
        "filename": "2025/README.markdown",
        "status": "added",
        "additions": 5,
        "deletions": 0,
        "changes": 5,
        "blob_url": "https://github.com/hestonhoffman/tob_randomizer/blob/4ea5af5845607ca48eb9fbfd486c8ba4e907462f/2025%2FREADME.markdown",
        "raw_url": "https://github.com/hestonhoffman/tob_randomizer/raw/4ea5af5845607ca48eb9fbfd486c8ba4e907462f/2025%2FREADME.markdown",
        "contents_url": "https://api.github.com/repos/hestonhoffman/tob_randomizer/contents/2025%2FREADME.markdown?ref=4ea5af5845607ca48eb9fbfd486c8ba4e907462f",
        "patch": "@@ -0,0 +1,5 @@\n+To create a randomized TOB bracket, clone this repo and run this command:\n+\n+```ruby\n+ruby tob.rb\n+```"
    },
    {
        "sha": "e69fbb035df9d1a9b77928aa470d82fc856194ad",
        "filename": "2025/books.yaml",
        "status": "added",
        "additions": 28,
        "deletions": 0,
        "changes": 28,
        "blob_url": "https://github.com/hestonhoffman/tob_randomizer/blob/4ea5af5845607ca48eb9fbfd486c8ba4e907462f/2025%2Fbooks.yaml",
        "raw_url": "https://github.com/hestonhoffman/tob_randomizer/raw/4ea5af5845607ca48eb9fbfd486c8ba4e907462f/2025%2Fbooks.yaml",
        "contents_url": "https://api.github.com/repos/hestonhoffman/tob_randomizer/contents/2025%2Fbooks.yaml?ref=4ea5af5845607ca48eb9fbfd486c8ba4e907462f",
        "patch": "@@ -0,0 +1,28 @@\n+S1:\n+  1: \n+  4: \n+  2: \n+  3: \n+\n+S2:\n+  1: \n+  4: \n+  2: \n+  3: \n+\n+S3:\n+  1: \n+  4: \n+  2: \n+  3: \n+\n+S4:\n+  1: \n+  4: \n+  2: \n+  3: \n+\n+Play-ins:\n+  - \n+  - \n+  - "
    },
    {
        "sha": "0f3b1de655a1a05b720aa03e0f7ab947ee2fa0d2",
        "filename": "2025/color.rb",
        "status": "added",
        "additions": 30,
        "deletions": 0,
        "changes": 30,
        "blob_url": "https://github.com/hestonhoffman/tob_randomizer/blob/4ea5af5845607ca48eb9fbfd486c8ba4e907462f/2025%2Fcolor.rb",
        "raw_url": "https://github.com/hestonhoffman/tob_randomizer/raw/4ea5af5845607ca48eb9fbfd486c8ba4e907462f/2025%2Fcolor.rb",
        "contents_url": "https://api.github.com/repos/hestonhoffman/tob_randomizer/contents/2025%2Fcolor.rb?ref=4ea5af5845607ca48eb9fbfd486c8ba4e907462f",
        "patch": "@@ -0,0 +1,30 @@\n+class String\n+    # colorization\n+    def colorize(color_code)\n+      \"\\e[#{color_code}m#{self}\\e[0m\"\n+    end\n+  \n+    def red\n+      colorize(31)\n+    end\n+  \n+    def green\n+      colorize(32)\n+    end\n+  \n+    def yellow\n+      colorize(33)\n+    end\n+  \n+    def blue\n+      colorize(34)\n+    end\n+  \n+    def pink\n+      colorize(35)\n+    end\n+  \n+    def light_blue\n+      colorize(36)\n+    end\n+end\n\\ No newline at end of file"
    }
]

TEST_MODIFIED_ANSWER = {
    '2025/README.markdown': 
        [['1,5', '+To create a randomized TOB bracket, clone this repo and run this command:', '+', '+```ruby', '+ruby tob.rb', '+```']],
    '2025/books.yaml': 
        [['1,28', '+S1:', '+  1: ', '+  4: ', '+  2: ', '+  3: ', '+', '+S2:', '+  1: ', '+  4: ', '+  2: ', '+  3: ', '+', '+S3:', '+  1: ', '+  4: ', '+  2: ', '+  3: ', '+', '+S4:', '+  1: ', '+  4: ', '+  2: ', '+  3: ', '+', '+Play-ins:', '+  - ', '+  - ', '+  - ']],
    '2025/color.rb': 
        [['1,30', '+class String', '+    # colorization', '+    def colorize(color_code)', '+      "\\e[#{color_code}m#{self}\\e[0m"', '+    end', '+  ', '+    def red', '+      colorize(31)', '+    end', '+  ', '+    def green', '+      colorize(32)', '+    end', '+  ', '+    def yellow', '+      colorize(33)', '+    end', '+  ', '+    def blue', '+      colorize(34)', '+    end', '+  ', '+    def pink', '+      colorize(35)', '+    end', '+  ', '+    def light_blue', '+      colorize(36)', '+    end', '+end']]
}

STATUS_NO_PATCH = [{
    "sha": "1234",
    "filename": "some/file.somefile",
    "status": "added",
    "additions": 1000,
    "deletions": 100,
    "changes": 100,
    "blob_url": "https://example.com",
    "raw_url": "https://example.com",
    "contents_url": "https://example.com"
}]

TEST_GET_LINES_ANSWER = {
    '2025/README.markdown': [1, 2, 3, 4, 5], 
    '2025/books.yaml': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28],
    '2025/color.rb': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]}