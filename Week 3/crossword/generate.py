import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Take a var for all in self.domains, check its length, and remove any word from the domain which does not equal that domain

        for var in self.domains:
            length = var.length

            delete = []
            for word in self.domains[var]:
                if len(word) != length:
                    delete.append(word)
            
            for word in delete:
                self.domains[var].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revision = False
        
        """
        for a variable -> i, j, direction, length
        """
        """
        Check if both of these variables overlap. If they don't, return false
        If the variables overlap, check where do they overlap -> look what which letter for x overlaps with which letter with y.
        Then, for each word in x, see if there is at lease one word in y wherein x's ith letter is the same as y's jth letter.
        If not, then remove that word from x's self.domain
        """
        if self.crossword.overlaps[x,y] == None:
            return revision
        else:
            i, j = self.crossword.overlaps[x, y]

            removelist = []
            for word_x in self.domains[x]:
                remove = True
                for word_y in self.domains[y]:
                    if word_x[i] == word_y[j]:
                        remove = False
                        break
                
                if remove:
                    removelist.append(word_x)

            for word_x in removelist:
                self.domains[x].remove(word_x)
                revision = True

        return revision
                        
        
    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        
        """
        Check if arcs == None.
        If it is None, create a list (queue) with all possible arcs, using the keys of self.domains

        If arcs != None,
        Assign the variable queue to arcs so that the remaining logic remains the same
        """
        if arcs == None:
            queue = []
            for var1 in self.domains:
                for var2 in self.domains:
                    if var1 == var2:
                        continue
                    else:
                        queue.append((var1, var2))
        else:
            queue = arcs
        
        """
        while queue non-empty:
            (X, Y) = Dequeue(queue)
            if Revise(csp, X, Y):
                if size of X.domain == 0:
                    return false
                for each Z in X.neighbors - {Y}:
                    Enqueue(queue, (Z,X))
        return true 
        """
        while queue != []:
            x, y = queue.pop()
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                for var in self.crossword.neighbors(x):
                    if var == x:
                        continue
                    else:
                        queue.append((var, x))
        
        return True
            

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for var in self.domains:
            if assignment[var] == None:
                return False
        
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        """
        For each variable in self.domains, if there is an assignment:
            Create a dict name called duplicate, and add this word to it with value 1
            Check if it matches the length of the variable
            Fetch neighbours
            For each neighbour, check if ith letter = jth letter
        """
        duplicate = []

        if assignment == None:
            return True

        for var in assignment:
            if assignment[var] in duplicate:
                return False
            else:
                duplicate.append(assignment[var])

            if var.length != len(assignment[var]):
                return False

            neighbor = self.crossword.neighbors(var)

            for y in neighbor:
                i, j = self.crossword.overlaps[var, y]

                if y not in assignment:
                    continue
                elif assignment[var][i] != assignment[y][j]:
                    return False
            
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        return self.domains[var]

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        for var in self.domains:
            if var not in assignment:
                return var

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        """
        if assignment complete:
            return assignment
        var = Select-Unassigned-Var(assignment, csp)
        for value in Domain-Values(var, assignment, csp):
            if value consistent with assignment:
                add {var = value} to assignment
                result = Backtrack(assignment, csp)
                if result ≠ failure:
                    return result
                remove {var = value} from assignment
        return failure
        """
        if len(assignment.keys()) == len(self.domains.keys()):
            return assignment
        
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            dummy = assignment.copy()
            dummy[var] = value
            if self.consistent(dummy):
                assignment[var] = value
                result = self.backtrack(assignment)
                if self.consistent(result):
                    return assignment
                assignment.pop(var)
        
        return None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Hard coded values
    # structure = "data/structure1.txt"
    # words = "data/words1.txt"
    # output = "output.png"

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
