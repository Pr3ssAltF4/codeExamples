package perp.tree;

import perp.SymbolTable;

/**
 * An abstraction for all PerpNodes that can be evaluated to
 * get a value back. By definition they do not alter the "state"
 * (symbol table) of the program when evaluated.
 *
 * @author James Heliotis
 */
public interface ExpressionNode extends PerpNode {
    /**
     * Evaluate the expression represented by this node.
     *
     * @param symTab symbol table, if needed, to fetch variable values
     * @return the result of the evaluation
     */
    int evaluate( SymbolTable symTab );
}
