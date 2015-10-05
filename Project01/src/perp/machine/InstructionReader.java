package perp.machine;

import perp.machine.stu.Machine;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.*;
import java.util.function.Function;

/**
 * Assemble instructions from a file.
 * This is a project debugging aid.
 *
 * @author James Heliotis
 */
public class InstructionReader {

    private static Map< String, Function< Scanner, Machine.Instruction> > gen
            = new HashMap< String, Function< Scanner, Machine.Instruction > >()
    {{
        put( "PUSH", in -> { int i = in.nextInt();
                             return new Machine.PushConst( i ); } );
        put( "LOAD", in -> { String v = in.next();
                             return new Machine.Load( v ); } );
        put( "STORE", in -> { String v = in.next();
                              return new Machine.Store( v ); } );
        put( "ADD", in -> new Machine.Add() );
        put( "SUB", in -> new Machine.Subtract() );
        put( "MUL", in -> new Machine.Multiply() );
        put( "DIV", in -> new Machine.Divide() );
        put( "NEG", in -> new Machine.Negate() );
        put( "SQRT", in -> new Machine.SquareRoot() );
        put( "PRINT", in -> new Machine.Print() );
    }};

    /**
     * Read instructions from the named file and translate them
     * to internal form.
     * @param assyFile the name of the text file containing the assembly code
     * @return a list of Machine.Instruction objects, ready to execute
     */
    public static List< Machine.Instruction > assemble( String assyFile ) {
        try ( FileInputStream fileStr = new FileInputStream( assyFile ) ) {
            List< Machine.Instruction > result = new LinkedList<>();
            Scanner in = new Scanner( fileStr );
            while ( in.hasNext() ) {
                String mnemonic = in.next();
                if ( gen.containsKey( mnemonic ) ) {
                    result.add( gen.get( mnemonic ).apply( in ) );
                }
                else {
                    System.err.println( "Illegal assembly instr " + mnemonic );
                }
            }
            return result;
        }
        catch( IOException ioe ) {
            System.err.println( "Could not open file " + assyFile );
        }
        return null;
    }

    /**
     * Assemble and execute some Perp machine code.
     * @param args the name of the assembly language source file
     */
    public static void main( String[] args ) {
        if ( args.length != 1 ) {
            System.err.println(
                    "Usage: java InstructionReader assembly-code-file" );
            System.exit( 1 );
        }
        List< Machine.Instruction > code = assemble( args[ 0 ] );
        Machine.execute( code );
    }
}
