#ifndef MATRIX_ENGINE_H
#define MATRIX_ENGINE_H

#include <Eigen/Dense>
#include <Eigen/Eigenvalues>
#include <vector>
#include <string>
#include <iostream>
#include <stdexcept>

using namespace Eigen;

/**
 * MatrixEngine - Comprehensive matrix operations library using Eigen
 * Designed for AI/ML learning and numerical linear algebra
 */
class MatrixEngine {
private:
    MatrixXd matrix;
    int rows;
    int cols;

public:
    // ========== Constructors & Initialization ==========
    
    /**
     * Default constructor - creates empty matrix
     */
    MatrixEngine();
    
    /**
     * Constructor with dimensions
     * @param rows Number of rows
     * @param cols Number of columns
     */
    MatrixEngine(int rows, int cols);
    
    /**
     * Constructor from Eigen matrix
     * @param mat Eigen matrix
     */
    MatrixEngine(const MatrixXd& mat);
    
    /**
     * Constructor from 2D vector
     * @param data 2D vector of doubles
     */
    MatrixEngine(const std::vector<std::vector<double>>& data);
    
    /**
     * Create identity matrix
     * @param size Dimension of identity matrix
     * @return MatrixEngine containing identity matrix
     */
    static MatrixEngine identity(int size);
    
    /**
     * Create zero matrix
     * @param rows Number of rows
     * @param cols Number of columns
     * @return MatrixEngine containing zero matrix
     */
    static MatrixEngine zeros(int rows, int cols);
    
    /**
     * Create ones matrix
     * @param rows Number of rows
     * @param cols Number of columns
     * @return MatrixEngine containing ones matrix
     */
    static MatrixEngine ones(int rows, int cols);
    
    /**
     * Create random matrix with values between 0 and 1
     * @param rows Number of rows
     * @param cols Number of columns
     * @return MatrixEngine containing random matrix
     */
    static MatrixEngine random(int rows, int cols);
    
    // ========== Input/Output Operations ==========
    
    /**
     * Set value at specific position
     * @param row Row index (0-based)
     * @param col Column index (0-based)
     * @param value Value to set
     */
    void setValue(int row, int col, double value);
    
    /**
     * Get value at specific position
     * @param row Row index (0-based)
     * @param col Column index (0-based)
     * @return Value at position
     */
    double getValue(int row, int col) const;
    
    /**
     * Input matrix values from console
     */
    void inputMatrix();
    
    /**
     * Display matrix in formatted way
     * @param precision Number of decimal places
     */
    void display(int precision = 4) const;
    
    /**
     * Get string representation of matrix
     * @param precision Number of decimal places
     * @return String representation
     */
    std::string toString(int precision = 4) const;
    
    /**
     * Get dimensions
     */
    int getRows() const { return rows; }
    int getCols() const { return cols; }
    
    /**
     * Get underlying Eigen matrix
     */
    const MatrixXd& getMatrix() const { return matrix; }
    
    // ========== Basic Matrix Operations ==========
    
    /**
     * Matrix addition
     * @param other Matrix to add
     * @return Result of addition
     */
    MatrixEngine add(const MatrixEngine& other) const;
    
    /**
     * Matrix subtraction
     * @param other Matrix to subtract
     * @return Result of subtraction
     */
    MatrixEngine subtract(const MatrixEngine& other) const;
    
    /**
     * Matrix multiplication
     * @param other Matrix to multiply with
     * @return Result of multiplication
     */
    MatrixEngine multiply(const MatrixEngine& other) const;
    
    /**
     * Scalar multiplication
     * @param scalar Scalar value
     * @return Result of scalar multiplication
     */
    MatrixEngine scalarMultiply(double scalar) const;
    
    /**
     * Element-wise multiplication (Hadamard product)
     * @param other Matrix for element-wise multiplication
     * @return Result of element-wise multiplication
     */
    MatrixEngine elementwiseMultiply(const MatrixEngine& other) const;
    
    /**
     * Matrix transpose
     * @return Transposed matrix
     */
    MatrixEngine transpose() const;
    
    /**
     * Matrix trace (sum of diagonal elements)
     * @return Trace value
     */
    double trace() const;
    
    // ========== Advanced Matrix Operations ==========
    
    /**
     * Matrix determinant
     * @return Determinant value
     */
    double determinant() const;
    
    /**
     * Matrix inverse
     * @return Inverse matrix
     * @throws std::runtime_error if matrix is not invertible
     */
    MatrixEngine inverse() const;
    
    /**
     * Check if matrix is invertible
     * @return true if invertible, false otherwise
     */
    bool isInvertible() const;
    
    /**
     * Matrix rank
     * @return Rank of matrix
     */
    int rank() const;
    
    /**
     * Matrix condition number (ratio of largest to smallest singular value)
     * @return Condition number
     */
    double conditionNumber() const;
    
    /**
     * Matrix norm (Frobenius norm by default)
     * @return Norm value
     */
    double norm() const;
    
    // ========== Row Reduction ==========
    
    /**
     * Row Echelon Form (REF)
     * @return Matrix in REF
     */
    MatrixEngine rowEchelonForm() const;
    
    /**
     * Reduced Row Echelon Form (RREF)
     * @return Matrix in RREF
     */
    MatrixEngine reducedRowEchelonForm() const;
    
    // ========== Eigenvalue & Eigenvector Operations ==========
    
    /**
     * Compute eigenvalues
     * @return Vector of eigenvalues (may be complex)
     */
    std::vector<std::complex<double>> eigenvalues() const;
    
    /**
     * Compute real eigenvalues (only for symmetric matrices)
     * @return Vector of real eigenvalues
     */
    std::vector<double> realEigenvalues() const;
    
    /**
     * Compute eigenvectors
     * @return Matrix where each column is an eigenvector
     */
    MatrixEngine eigenvectors() const;
    
    /**
     * Compute eigendecomposition (for symmetric matrices)
     * @param eigenvals Output vector for eigenvalues
     * @param eigenvecs Output matrix for eigenvectors
     */
    void eigenDecomposition(std::vector<double>& eigenvals, MatrixEngine& eigenvecs) const;
    
    // ========== Matrix Decompositions ==========
    
    /**
     * Singular Value Decomposition (SVD)
     * A = U * Σ * V^T
     * @param U Left singular vectors
     * @param S Singular values (diagonal)
     * @param V Right singular vectors
     */
    void svd(MatrixEngine& U, MatrixEngine& S, MatrixEngine& V) const;
    
    /**
     * Get singular values only
     * @return Vector of singular values
     */
    std::vector<double> singularValues() const;
    
    /**
     * LU Decomposition
     * A = L * U (with partial pivoting: P*A = L*U)
     * @param L Lower triangular matrix
     * @param U Upper triangular matrix
     * @param P Permutation matrix
     */
    void luDecomposition(MatrixEngine& L, MatrixEngine& U, MatrixEngine& P) const;
    
    /**
     * QR Decomposition
     * A = Q * R
     * @param Q Orthogonal matrix
     * @param R Upper triangular matrix
     */
    void qrDecomposition(MatrixEngine& Q, MatrixEngine& R) const;
    
    /**
     * Cholesky Decomposition (for positive definite matrices)
     * A = L * L^T
     * @return Lower triangular matrix L
     */
    MatrixEngine choleskyDecomposition() const;
    
    // ========== Vector Operations ==========
    
    /**
     * Dot product (for vectors - single row or column)
     * @param other Vector to compute dot product with
     * @return Dot product value
     */
    double dotProduct(const MatrixEngine& other) const;
    
    /**
     * Cross product (for 3D vectors only)
     * @param other Vector to compute cross product with
     * @return Cross product vector
     */
    MatrixEngine crossProduct(const MatrixEngine& other) const;
    
    /**
     * Vector magnitude/length
     * @return Magnitude
     */
    double magnitude() const;
    
    /**
     * Normalize vector (unit vector)
     * @return Normalized vector
     */
    MatrixEngine normalize() const;
    
    /**
     * Check if this is a vector (single row or column)
     * @return true if vector, false otherwise
     */
    bool isVector() const;
    
    // ========== Orthogonalization ==========
    
    /**
     * Gram-Schmidt orthogonalization
     * Converts columns of matrix into orthonormal basis
     * @return Matrix with orthonormal columns
     */
    MatrixEngine gramSchmidt() const;
    
    /**
     * Modified Gram-Schmidt (more numerically stable)
     * @return Matrix with orthonormal columns
     */
    MatrixEngine modifiedGramSchmidt() const;
    
    // ========== Matrix Properties ==========
    
    /**
     * Check if matrix is square
     */
    bool isSquare() const;
    
    /**
     * Check if matrix is symmetric
     */
    bool isSymmetric(double tolerance = 1e-10) const;
    
    /**
     * Check if matrix is orthogonal (Q^T * Q = I)
     */
    bool isOrthogonal(double tolerance = 1e-10) const;
    
    /**
     * Check if matrix is diagonal
     */
    bool isDiagonal(double tolerance = 1e-10) const;
    
    /**
     * Check if matrix is upper triangular
     */
    bool isUpperTriangular(double tolerance = 1e-10) const;
    
    /**
     * Check if matrix is lower triangular
     */
    bool isLowerTriangular(double tolerance = 1e-10) const;
    
    /**
     * Check if matrix is positive definite
     */
    bool isPositiveDefinite() const;
    
    // ========== Utility Operations ==========
    
    /**
     * Extract a submatrix
     * @param startRow Starting row index
     * @param startCol Starting column index
     * @param numRows Number of rows to extract
     * @param numCols Number of columns to extract
     * @return Submatrix
     */
    MatrixEngine submatrix(int startRow, int startCol, int numRows, int numCols) const;
    
    /**
     * Get specific row as a matrix
     * @param rowIndex Row index
     * @return Row as matrix
     */
    MatrixEngine getRow(int rowIndex) const;
    
    /**
     * Get specific column as a matrix
     * @param colIndex Column index
     * @return Column as matrix
     */
    MatrixEngine getColumn(int colIndex) const;
    
    /**
     * Solve linear system Ax = b
     * @param b Right-hand side vector
     * @return Solution vector x
     */
    MatrixEngine solve(const MatrixEngine& b) const;
    
    /**
     * Matrix power (only for square matrices)
     * @param power Exponent
     * @return Matrix raised to power
     */
    MatrixEngine power(int power) const;
    
    /**
     * Concatenate matrices horizontally [A | B]
     * @param other Matrix to concatenate
     * @return Concatenated matrix
     */
    MatrixEngine hconcat(const MatrixEngine& other) const;
    
    /**
     * Concatenate matrices vertically [A; B]
     * @param other Matrix to concatenate
     * @return Concatenated matrix
     */
    MatrixEngine vconcat(const MatrixEngine& other) const;
    
    // ========== Operator Overloads ==========
    
    MatrixEngine operator+(const MatrixEngine& other) const;
    MatrixEngine operator-(const MatrixEngine& other) const;
    MatrixEngine operator*(const MatrixEngine& other) const;
    MatrixEngine operator*(double scalar) const;
    friend MatrixEngine operator*(double scalar, const MatrixEngine& mat);
    
    // ========== Static Utility Functions ==========
    
    /**
     * Check if two matrices are approximately equal
     */
    static bool approximatelyEqual(const MatrixEngine& a, const MatrixEngine& b, double tolerance = 1e-10);
};

#endif // MATRIX_ENGINE_H
