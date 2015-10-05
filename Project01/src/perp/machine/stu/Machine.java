package perp.machine.stu;

import java.util.List;
import java.util.Stack;
import perp.SymbolTable;
import perp.Errors;

/**
 * An abstraction of a computing machine that reads instructions
 * and executes them. It has an instruction set, a symbol table
 * for variables (instead of general-purpose memory), and a
 * value stack on which calculations are performed.
 *
 * (Everything is static to avoid the need to master the subtleties
 * of nested class instantiation or to pass the symbol table and
 * stack into every instruction when it executes.)
 *
 * THIS CLASS IS INCOMPLETE. The student must add code to it.
 *
 * @author James Heliotis
 * @author YOUR NAME HERE
 */
public class Machine {

    /** Do not instatiate this class. */
    private Machine() {}

    public static interface Instruction {
        /**
         * Run this instruction on the Machine, using the Machine's
         * value stack and symbol table.
         */
        void execute();

        /**
         * Show the instruction using text so it can be understood
         * by a person.
         * @return a short string describing what this instruction will do
         */
        @Override
        String toString();
    }

    private static SymbolTable table = null;
    private static Stack< Integer > stack = null;

    /**
     * Reset the Machine to a pristine state.
     * @see Machine#execute
     */
    private static void reset() {
        stack = new Stack<Integer>();
        table = new SymbolTable();
    }

    /**
     * Generate a listing of a program on standard output by
     * calling the toString() method on each instruction
     * contained therein, in order.
     *
     * @param program the list of instructions in the program
     */
    public static void displayInstructions(
            List< Machine.Instruction > program ) {
        System.out.println( "\nCompiled code:" );
        for ( Machine.Instruction instr: program ) {
            System.out.println( instr );
        }
        System.out.println();
    }

    /**
     * Run a "compiled" program by executing in order each instruction
     * contained therein.
     * Report on the final size of the stack (should normally be empty)
     * and the contents of the symbol table.
     * @param program a list of Machine instructions
     */
    public static void execute( List< Instruction > program ) {
        reset();
        System.out.println("Executing compiled code...");
        for ( Instruction instr: program ) {
            instr.execute();
        }
        System.out.println( "Machine: execution ended with " +
                stack.size() + " items left on the stack." );
        System.out.println();
        table.dump();
    }

    /**
     * The ADD instruction
     */
    public static class Add implements Instruction {
        /**
         * Run the microsteps for the ADD instruction.
         */
        @Override
        public void execute() {
            int op2 = stack.pop();
            int op1 = stack.pop();
            stack.push( op1 + op2 );
        }

        /**
         * Show the ADD instruction as plain text.
         * @return "ADD"
         */
        @Override
        public String toString() {
            return "ADD";
        }
    }

    /**
     * The STORE instruction
     */
    public static class Store implements Instruction {
        /** stores name of target variable */
        private String name;

        /**
         * Create a STORE instruction
         * @param ident the name of the target variable
         */
        public Store( String ident ) {
            this.name = ident;
        }
        /**
         * Run the microsteps for the STORE instruction.
         */
        @Override
        public void execute() {
            table.put( this.name, stack.pop() );
        }
        /**
         * Show the STORE instruction as plain text.
         * @return "STORE" followed by the target variable name
         */
        @Override
        public String toString() {
            return "STORE " + this.name;
        }
    }

    //
    // ENTER YOUR CODE FOR THE OTHER INSTRUCTION CLASSES HERE.
    //

    public static class Load implements Instruction {

        private String name;

        public Load (String name) {this.name = name;}

        @Override
        public void execute() {
            if(table.exists(name))
                stack.push(table.get(name));
            else {
                Errors.error("Variable does not exist.", table);
            }
        }

        @Override
        public String toString() {
            return "LOAD " + this.name;
        }

    }

    public static class Subtract implements Instruction {
        @Override
        public void execute () {
            int op1 = stack.pop();
            int op2 = stack.pop();
            stack.push(op1 - op2);
        }

        @Override
        public String toString() {
            return "SUB";
        }
    }

    public static class Negate implements Instruction {
        @Override
        public void execute () {
            int op1 = stack.pop();
            stack.push(Math.abs(0 - op1));
        }

        @Override
        public String toString() {
            return "NEG";
        }
    }

    public static class Divide implements Instruction {
        @Override
        public void execute () {
            int op1 = stack.pop();
            int op2 = stack.pop();
            stack.push(op1 / op2);
        }

        @Override
        public String toString() {
            return "DIV";
        }
    }

    public static class Print implements Instruction {
        @Override
        public void execute () {
            System.out.println("*** " + stack.pop());
        }

        @Override
        public String toString() {
            return "PRINT";
        }
    }

    public static class PushConst implements Instruction {
        private int c;
        public PushConst(int c) {this.c = c;}
        @Override
        public void execute () {
            stack.push(c);
        }

        @Override
        public String toString() {
            return "PUSH  " + c;
        }
    }

    public static class SquareRoot implements Instruction {
        @Override
        public void execute () {
            int op1 = stack.pop();
            stack.push((int)Math.sqrt((double)op1));
        }

        @Override
        public String toString() {
            return "SQRT";
        }
    }

    public static class Multiply implements Instruction {
        @Override
        public void execute () {
            int op1 = stack.pop();
            int op2 = stack.pop();
            stack.push(op1 * op2);
        }

        @Override
        public String toString() {
            return "MULT";
        }
    }
}
