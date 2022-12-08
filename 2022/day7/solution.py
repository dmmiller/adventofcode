from dataclasses import dataclass, field

data = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

with open("input.txt") as f:
    data = f.read()


@dataclass
class File:
    name: str
    size: int


@dataclass
class Directory:
    name: str
    parent: 'Directory'
    contents: dict[str, object] = field(default_factory=dict)

    def addFile(self, file: File):
        assert (file.name not in self.contents)
        self.contents[file.name] = file

    def addDirectory(self, directory: 'Directory'):
        assert (directory.name not in self.contents)
        self.contents[directory.name] = directory

    def size(self):
        def computeSize(x):
            if isinstance(x, File):
                return x.size
            else:
                return x.size()
        return sum(map(computeSize, self.contents.values()))

    def yieldMatches(self, filter):
        for entry in self.contents.values():
            if filter(entry):
                yield entry
            if isinstance(entry, Directory):
                for match in entry.yieldMatches(filter):
                    yield match


root = Directory("/", None)
currentDirectory = root

lines = [line for line in data.splitlines()]
i = 0
while i < len(lines):
    assert (lines[i].startswith("$ "))
    cmd = lines[i][2:]
    if cmd.startswith("ls"):
        i += 1
        while i < len(lines) and not lines[i].startswith("$"):
            entry = lines[i]
            left, right = entry.split(" ")
            if (left == "dir"):
                currentDirectory.addDirectory(
                    Directory(right, currentDirectory))
            else:
                currentDirectory.addFile(File(right, int(left)))

            i += 1
    else:
        assert (cmd.startswith("cd"))
        target = cmd[3:]
        if (target == "/"):
            currentDirectory = root
        elif (target == ".."):
            currentDirectory = currentDirectory.parent
        else:
            currentDirectory = currentDirectory.contents[target]
        i += 1

total = 0
for match in root.yieldMatches(lambda x: False if isinstance(x, File) else x.size() <= 100000):
    total += match.size()
print(f"Part 1 : Total size of all directories <= 100000 bytes is {total}")

partition_size = 70000000
minimum_needed = 30000000

current_unused = partition_size - root.size()
need_to_delete = minimum_needed - current_unused

print(
    f"Part 2: Smallest directory to delete has size: {sorted((match for match in root.yieldMatches(lambda x: False if isinstance(x, File) else x.size() >= need_to_delete)), key=lambda x: x.size())[0].size()}")
