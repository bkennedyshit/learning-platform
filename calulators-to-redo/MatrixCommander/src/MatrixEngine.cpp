#include "MatrixEngine.h"
#include <iomanip>
#include <sstream>
#include <cmath>
#include <algorithm>

// ========== Constructors & Initialization ==========

MatrixEngine::MatrixEngine() : rows(0), cols(0) {
    matrix = MatrixXd(0, 0);
}

MatrixEngine::MatrixEngine(int rows, int cols) : rows(rows), cols(cols) {
    if (rows <= 0 || cols <= 0) {
        throw std::invalid_argument("Matrix dimensions must be positive");
    }
    matrix = MatrixXd::Zero(rows, cols);
}

MatrixEngine::MatrixEngine(const MatrixXd& mat) {
    matrix = mat;
    rows = mat.rows();
    cols = mat.cols();
}

MatrixEngine::MatrixEngine(const std::vector<std::vector<double>>& data) {
    if (data.empty() || data[0].empty()) {
        throw std::invalid_argument("Cannot create matrix from empty data");
    }
    
    rows = data.size();
    cols = data[0].size();
    matrix = MatrixXd(rows, cols);
    
    for (int i = 0; i < rows; i++) {
        if (data[i].size() != cols) {
            throw std::invalid_argument("All rows must have the same number of columns");
        }
        for (int j = 0; j < cols; j++) {
            matrix(i, j) = data[i][j];
        }
    }
}

MatrixEngine MatrixEngine::identity(int size) {
    if (size <= 0) {
        throw std::invalid_argument("Identity matrix size must be positive");
    }
    return MatrixEngine(MatrixXd::Identity(size, size));
}

MatrixEngine MatrixEngine::zeros(int rows, int cols) {
    if (rows <= 0 || cols <= 0) {
        throw std::invalid_argument("Matrix dimensions must be positive");
    }
    return MatrixEngine(MatrixXd::Zero(rows, cols));
}

MatrixEngine MatrixEngine::ones(int rows, int cols) {
    if (rows <= 0 || cols <= 0) {
        throw std::invalid_argument("Matrix dimensions must be positive");
    }
    return MatrixEngine(MatrixXd::Ones(rows, cols));
}

MatrixEngine MatrixEngine::random(int rows, int cols) {
    if (rows <= 0 || cols <= 0) {
        throw std::invalid_argument("Matrix dimensions must be positive");
    }
    return MatrixEngine(MatrixXd::Random(rows, cols));
}

// ========== Input/Output Operations ==========

void MatrixEngine::setValue(int row, int col, double value) {
    if (row < 0 || row >= rows || col < 0 || col >= cols) {
        throw std::out_of_range("Matrix indices out of range");
    }
    matrix(row, col) = value;
}

double MatrixEngine::getValue(int row, int col) const {
    if (row < 0 || row >= rows || col < 0 || col >= cols) {
        throw std::out_of_range("Matrix indices out of range");
    }
    return matrix(row, col);
}

void MatrixEngine::inputMatrix() {
    std::cout << "Enter matrix values (" << rows << "x" << cols << "):\n";
    for (int i = 0; i < rows; i++) {
        std::cout << "Row " << (i + 1) << ": ";
        for (int j = 0; j < cols; j++) {
            std::cin >> matrix(i, j);
        }
    }
}

void MatrixEngine::display(int precision) const {
    std::cout << std::fixed << std::setprecision(precision);
    std::cout << matrix << std::endl;
}

std::string MatrixEngine::toString(int precision) const {
    std::stringstream ss;
    ss << std::fixed << std::setprecision(precision);
    ss << matrix;
    return ss.str();
}

// ========== Basic Matrix Operations ==========

MatrixEngine MatrixEngine::add(const MatrixEngine& other) const {
    if (rows != other.rows || cols != other.cols) {
        throw std::invalid_argument("Matrix dimensions must match for addition");
    }
    return MatrixEngine(matrix + other.matrix);
}

MatrixEngine MatrixEngine::subtract(const MatrixEngine& other) const {
    if (rows != other.rows || cols != other.cols) {
        throw std::invalid_argument("Matrix dimensions must match for subtraction");
    }
    return MatrixEngine(matrix - other.matrix);
}

MatrixEngine MatrixEngine::multiply(const MatrixEngine& other) const {
    if (cols != other.rows) {
        throw std::invalid_argument("Matrix dimensions incompatible for multiplication");
    }
    return MatrixEngine(matrix * other.matrix);
}

MatrixEngine MatrixEngine::scalarMultiply(double scalar) const {
    return MatrixEngine(matrix * scalar);
}

MatrixEngine MatrixEngine::elementwiseMultiply(const MatrixEngine& other) const {
    if (rows != other.rows || cols != other.cols) {
        throw std::invalid_argument("Matrix dimensions must match for element-wise multiplication");
    }
    return MatrixEngine(matrix.cwiseProduct(other.matrix));
}

MatrixEngine MatrixEngine::transpose() const {
    return MatrixEngine(matrix.transpose());
}

double MatrixEngine::trace() const {
    if (!isSquare()) {
        throw std::invalid_argument("Trace is only defined for square matrices");
    }
    return matrix.trace();
}

// ========== Advanced Matrix Operations ==========

double MatrixEngine::determinant() const {
    if (!isSquare()) {
        throw std::invalid_argument("Determinant is only defined for square matrices");
    }
    return matrix.determinant();
}

MatrixEngine MatrixEngine::inverse() const {
    if (!isSquare()) {
        throw std::invalid_argument("Inverse is only defined for square matrices");
    }
    
    if (!isInvertible()) {
        throw std::runtime_error("Matrix is singular (not invertible)");
    }
    
    return MatrixEngine(matrix.inverse());
}

bool MatrixEngine::isInvertible() const {
    if (!isSquare()) {
        return false;
    }
    
    double det = determinant();
    return std::abs(det) > 1e-10;
}

int MatrixEngine::rank() const {
    FullPivLU<MatrixXd> lu(matrix);
    return lu.rank();
}

double MatrixEngine::conditionNumber() const {
    JacobiSVD<MatrixXd> svd(matrix);
    VectorXd singularValues = svd.singularValues();
    
    if (singularValues.size() == 0) {
        return INFINITY;
    }
    
    double maxSV = singularValues(0);
    double minSV = singularValues(singularValues.size() - 1);
    
    if (std::abs(minSV) < 1e-15) {
        return INFINITY;
    }
    
    return maxSV / minSV;
}

double MatrixEngine::norm() const {
    return matrix.norm();
}

// ========== Row Reduction ==========

MatrixEngine MatrixEngine::rowEchelonForm() const {
    MatrixXd result = matrix;
    int lead = 0;
    
    for (int r = 0; r < rows; r++) {
        if (lead >= cols) {
            break;
        }
        
        int i = r;
        while (std::abs(result(i, lead)) < 1e-10) {
            i++;
            if (i == rows) {
                i = r;
                lead++;
                if (lead == cols) {
                    return MatrixEngine(result);
                }
            }
        }
        
        // Swap rows
        if (i != r) {
            result.row(i).swap(result.row(r));
        }
        
        // Scale pivot row
        double pivot = result(r, lead);
        if (std::abs(pivot) > 1e-10) {
            result.row(r) /= pivot;
        }
        
        // Eliminate below
        for (int i = r + 1; i < rows; i++) {
            double factor = result(i, lead);
            result.row(i) -= factor * result.row(r);
        }
        
        lead++;
    }
    
    return MatrixEngine(result);
}

MatrixEngine MatrixEngine::reducedRowEchelonForm() const {
    MatrixXd result = matrix;
    int lead = 0;
    
    for (int r = 0; r < rows; r++) {
        if (lead >= cols) {
            break;
        }
        
        int i = r;
        while (std::abs(result(i, lead)) < 1e-10) {
            i++;
            if (i == rows) {
                i = r;
                lead++;
                if (lead == cols) {
                    return MatrixEngine(result);
                }
            }
        }
        
        // Swap rows
        if (i != r) {
            result.row(i).swap(result.row(r));
        }
        
        // Scale pivot row
        double pivot = result(r, lead);
        if (std::abs(pivot) > 1e-10) {
            result.row(r) /= pivot;
        }
        
        // Eliminate above and below
        for (int i = 0; i < rows; i++) {
            if (i != r) {
                double factor = result(i, lead);
                result.row(i) -= factor * result.row(r);
            }
        }
        
        lead++;
    }
    
    return MatrixEngine(result);
}

// ========== Eigenvalue & Eigenvector Operations ==========

std::vector<std::complex<double>> MatrixEngine::eigenvalues() const {
    if (!isSquare()) {
        throw std::invalid_argument("Eigenvalues are only defined for square matrices");
    }
    
    EigenSolver<MatrixXd> solver(matrix);
    VectorXcd eigenvals = solver.eigenvalues();
    
    std::vector<std::complex<double>> result;
    for (int i = 0; i < eigenvals.size(); i++) {
        result.push_back(eigenvals(i));
    }
    
    return result;
}

std::vector<double> MatrixEngine::realEigenvalues() const {
    if (!isSquare()) {
        throw std::invalid_argument("Eigenvalues are only defined for square matrices");
    }
    
    if (!isSymmetric()) {
        throw std::invalid_argument("Real eigenvalues guaranteed only for symmetric matrices");
    }
    
    SelfAdjointEigenSolver<MatrixXd> solver(matrix);
    VectorXd eigenvals = solver.eigenvalues();
    
    std::vector<double> result;
    for (int i = 0; i < eigenvals.size(); i++) {
        result.push_back(eigenvals(i));
    }
    
    return result;
}

MatrixEngine MatrixEngine::eigenvectors() const {
    if (!isSquare()) {
        throw std::invalid_argument("Eigenvectors are only defined for square matrices");
    }
    
    EigenSolver<MatrixXd> solver(matrix);
    MatrixXcd eigenvecs_complex = solver.eigenvectors();
    
    // Convert to real (taking real part)
    MatrixXd eigenvecs_real = eigenvecs_complex.real();
    return MatrixEngine(eigenvecs_real);
}

void MatrixEngine::eigenDecomposition(std::vector<double>& eigenvals, MatrixEngine& eigenvecs) const {
    if (!isSquare()) {
        throw std::invalid_argument("Eigendecomposition is only defined for square matrices");
    }
    
    SelfAdjointEigenSolver<MatrixXd> solver(matrix);
    
    VectorXd vals = solver.eigenvalues();
    eigenvals.clear();
    for (int i = 0; i < vals.size(); i++) {
        eigenvals.push_back(vals(i));
    }
    
    eigenvecs = MatrixEngine(solver.eigenvectors());
}

// ========== Matrix Decompositions ==========

void MatrixEngine::svd(MatrixEngine& U, MatrixEngine& S, MatrixEngine& V) const {
    JacobiSVD<MatrixXd> svd(matrix, ComputeThinU | ComputeThinV);
    
    U = MatrixEngine(svd.matrixU());
    V = MatrixEngine(svd.matrixV());
    
    // Create diagonal matrix S
    VectorXd singularValues = svd.singularValues();
    int minDim = std::min(rows, cols);
    MatrixXd S_mat = MatrixXd::Zero(minDim, minDim);
    for (int i = 0; i < minDim; i++) {
        S_mat(i, i) = singularValues(i);
    }
    S = MatrixEngine(S_mat);
}

std::vector<double> MatrixEngine::singularValues() const {
    JacobiSVD<MatrixXd> svd(matrix);
    VectorXd sv = svd.singularValues();
    
    std::vector<double> result;
    for (int i = 0; i < sv.size(); i++) {
        result.push_back(sv(i));
    }
    
    return result;
}

void MatrixEngine::luDecomposition(MatrixEngine& L, MatrixEngine& U, MatrixEngine& P) const {
    if (!isSquare()) {
        throw std::invalid_argument("LU decomposition requires a square matrix");
    }
    
    PartialPivLU<MatrixXd> lu(matrix);
    
    L = MatrixEngine(lu.matrixLU().triangularView<Lower>());
    // Set diagonal of L to 1
    MatrixXd L_mat = L.matrix;
    for (int i = 0; i < rows; i++) {
        L_mat(i, i) = 1.0;
    }
    L = MatrixEngine(L_mat);
    
    U = MatrixEngine(lu.matrixLU().triangularView<Upper>());
    
    // Get permutation matrix
    MatrixXd P_mat = lu.permutationP();
    P = MatrixEngine(P_mat);
}

void MatrixEngine::qrDecomposition(MatrixEngine& Q, MatrixEngine& R) const {
    HouseholderQR<MatrixXd> qr(matrix);
    
    Q = MatrixEngine(qr.householderQ() * MatrixXd::Identity(rows, std::min(rows, cols)));
    R = MatrixEngine(qr.matrixQR().triangularView<Upper>());
}

MatrixEngine MatrixEngine::choleskyDecomposition() const {
    if (!isSquare()) {
        throw std::invalid_argument("Cholesky decomposition requires a square matrix");
    }
    
    if (!isSymmetric()) {
        throw std::invalid_argument("Cholesky decomposition requires a symmetric matrix");
    }
    
    if (!isPositiveDefinite()) {
        throw std::invalid_argument("Cholesky decomposition requires a positive definite matrix");
    }
    
    LLT<MatrixXd> llt(matrix);
    if (llt.info() != Success) {
        throw std::runtime_error("Cholesky decomposition failed");
    }
    
    return MatrixEngine(llt.matrixL());
}

// ========== Vector Operations ==========

double MatrixEngine::dotProduct(const MatrixEngine& other) const {
    if (!isVector() || !other.isVector()) {
        throw std::invalid_argument("Dot product is only defined for vectors");
    }
    
    int thisSize = std::max(rows, cols);
    int otherSize = std::max(other.rows, other.cols);
    
    if (thisSize != otherSize) {
        throw std::invalid_argument("Vectors must have the same dimension for dot product");
    }
    
    VectorXd v1, v2;
    if (rows == 1) {
        v1 = matrix.row(0).transpose();
    } else {
        v1 = matrix.col(0);
    }
    
    if (other.rows == 1) {
        v2 = other.matrix.row(0).transpose();
    } else {
        v2 = other.matrix.col(0);
    }
    
    return v1.dot(v2);
}

MatrixEngine MatrixEngine::crossProduct(const MatrixEngine& other) const {
    if (!isVector() || !other.isVector()) {
        throw std::invalid_argument("Cross product is only defined for vectors");
    }
    
    int thisSize = std::max(rows, cols);
    int otherSize = std::max(other.rows, other.cols);
    
    if (thisSize != 3 || otherSize != 3) {
        throw std::invalid_argument("Cross product is only defined for 3D vectors");
    }
    
    Vector3d v1, v2;
    if (rows == 1) {
        v1 = matrix.row(0).transpose();
    } else {
        v1 = matrix.col(0);
    }
    
    if (other.rows == 1) {
        v2 = other.matrix.row(0).transpose();
    } else {
        v2 = other.matrix.col(0);
    }
    
    Vector3d result = v1.cross(v2);
    
    // Return as column vector
    MatrixXd resultMat(3, 1);
    resultMat.col(0) = result;
    return MatrixEngine(resultMat);
}

double MatrixEngine::magnitude() const {
    if (!isVector()) {
        throw std::invalid_argument("Magnitude is only defined for vectors");
    }
    
    return matrix.norm();
}

MatrixEngine MatrixEngine::normalize() const {
    if (!isVector()) {
        throw std::invalid_argument("Normalization is only defined for vectors");
    }
    
    double mag = magnitude();
    if (std::abs(mag) < 1e-15) {
        throw std::runtime_error("Cannot normalize zero vector");
    }
    
    return MatrixEngine(matrix / mag);
}

bool MatrixEngine::isVector() const {
    return (rows == 1 || cols == 1);
}

// ========== Orthogonalization ==========

MatrixEngine MatrixEngine::gramSchmidt() const {
    if (rows < cols) {
        throw std::invalid_argument("Matrix must have at least as many rows as columns for Gram-Schmidt");
    }
    
    MatrixXd result = MatrixXd::Zero(rows, cols);
    
    for (int j = 0; j < cols; j++) {
        VectorXd v = matrix.col(j);
        
        // Subtract projections onto previous vectors
        for (int i = 0; i < j; i++) {
            VectorXd u = result.col(i);
            double proj = v.dot(u);
            v -= proj * u;
        }
        
        // Normalize
        double norm = v.norm();
        if (norm > 1e-15) {
            result.col(j) = v / norm;
        } else {
            // Linearly dependent vector, set to zero
            result.col(j) = VectorXd::Zero(rows);
        }
    }
    
    return MatrixEngine(result);
}

MatrixEngine MatrixEngine::modifiedGramSchmidt() const {
    if (rows < cols) {
        throw std::invalid_argument("Matrix must have at least as many rows as columns for Modified Gram-Schmidt");
    }
    
    MatrixXd result = matrix;
    
    for (int j = 0; j < cols; j++) {
        // Normalize current column
        double norm = result.col(j).norm();
        if (norm > 1e-15) {
            result.col(j) /= norm;
        } else {
            result.col(j) = VectorXd::Zero(rows);
            continue;
        }
        
        // Orthogonalize remaining columns
        for (int k = j + 1; k < cols; k++) {
            double proj = result.col(k).dot(result.col(j));
            result.col(k) -= proj * result.col(j);
        }
    }
    
    return MatrixEngine(result);
}

// ========== Matrix Properties ==========

bool MatrixEngine::isSquare() const {
    return rows == cols;
}

bool MatrixEngine::isSymmetric(double tolerance) const {
    if (!isSquare()) {
        return false;
    }
    
    return (matrix - matrix.transpose()).norm() < tolerance;
}

bool MatrixEngine::isOrthogonal(double tolerance) const {
    if (!isSquare()) {
        return false;
    }
    
    MatrixXd product = matrix.transpose() * matrix;
    MatrixXd identity = MatrixXd::Identity(rows, cols);
    
    return (product - identity).norm() < tolerance;
}

bool MatrixEngine::isDiagonal(double tolerance) const {
    if (!isSquare()) {
        return false;
    }
    
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            if (i != j && std::abs(matrix(i, j)) > tolerance) {
                return false;
            }
        }
    }
    
    return true;
}

bool MatrixEngine::isUpperTriangular(double tolerance) const {
    if (!isSquare()) {
        return false;
    }
    
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < i; j++) {
            if (std::abs(matrix(i, j)) > tolerance) {
                return false;
            }
        }
    }
    
    return true;
}

bool MatrixEngine::isLowerTriangular(double tolerance) const {
    if (!isSquare()) {
        return false;
    }
    
    for (int i = 0; i < rows; i++) {
        for (int j = i + 1; j < cols; j++) {
            if (std::abs(matrix(i, j)) > tolerance) {
                return false;
            }
        }
    }
    
    return true;
}

bool MatrixEngine::isPositiveDefinite() const {
    if (!isSquare() || !isSymmetric()) {
        return false;
    }
    
    LLT<MatrixXd> llt(matrix);
    return llt.info() == Success;
}

// ========== Utility Operations ==========

MatrixEngine MatrixEngine::submatrix(int startRow, int startCol, int numRows, int numCols) const {
    if (startRow < 0 || startCol < 0 || 
        startRow + numRows > rows || startCol + numCols > cols) {
        throw std::out_of_range("Submatrix indices out of range");
    }
    
    return MatrixEngine(matrix.block(startRow, startCol, numRows, numCols));
}

MatrixEngine MatrixEngine::getRow(int rowIndex) const {
    if (rowIndex < 0 || rowIndex >= rows) {
        throw std::out_of_range("Row index out of range");
    }
    
    return MatrixEngine(matrix.row(rowIndex));
}

MatrixEngine MatrixEngine::getColumn(int colIndex) const {
    if (colIndex < 0 || colIndex >= cols) {
        throw std::out_of_range("Column index out of range");
    }
    
    return MatrixEngine(matrix.col(colIndex));
}

MatrixEngine MatrixEngine::solve(const MatrixEngine& b) const {
    if (!isSquare()) {
        // Use least squares for non-square systems
        MatrixXd solution = matrix.colPivHouseholderQr().solve(b.matrix);
        return MatrixEngine(solution);
    }
    
    if (rows != b.rows) {
        throw std::invalid_argument("Incompatible dimensions for solving linear system");
    }
    
    MatrixXd solution = matrix.colPivHouseholderQr().solve(b.matrix);
    return MatrixEngine(solution);
}

MatrixEngine MatrixEngine::power(int power) const {
    if (!isSquare()) {
        throw std::invalid_argument("Matrix power is only defined for square matrices");
    }
    
    if (power < 0) {
        return inverse().power(-power);
    }
    
    if (power == 0) {
        return identity(rows);
    }
    
    if (power == 1) {
        return *this;
    }
    
    MatrixXd result = MatrixXd::Identity(rows, cols);
    MatrixXd base = matrix;
    
    while (power > 0) {
        if (power % 2 == 1) {
            result = result * base;
        }
        base = base * base;
        power /= 2;
    }
    
    return MatrixEngine(result);
}

MatrixEngine MatrixEngine::hconcat(const MatrixEngine& other) const {
    if (rows != other.rows) {
        throw std::invalid_argument("Matrices must have the same number of rows for horizontal concatenation");
    }
    
    MatrixXd result(rows, cols + other.cols);
    result << matrix, other.matrix;
    return MatrixEngine(result);
}

MatrixEngine MatrixEngine::vconcat(const MatrixEngine& other) const {
    if (cols != other.cols) {
        throw std::invalid_argument("Matrices must have the same number of columns for vertical concatenation");
    }
    
    MatrixXd result(rows + other.rows, cols);
    result << matrix, other.matrix;
    return MatrixEngine(result);
}

// ========== Operator Overloads ==========

MatrixEngine MatrixEngine::operator+(const MatrixEngine& other) const {
    return add(other);
}

MatrixEngine MatrixEngine::operator-(const MatrixEngine& other) const {
    return subtract(other);
}

MatrixEngine MatrixEngine::operator*(const MatrixEngine& other) const {
    return multiply(other);
}

MatrixEngine MatrixEngine::operator*(double scalar) const {
    return scalarMultiply(scalar);
}

MatrixEngine operator*(double scalar, const MatrixEngine& mat) {
    return mat.scalarMultiply(scalar);
}

// ========== Static Utility Functions ==========

bool MatrixEngine::approximatelyEqual(const MatrixEngine& a, const MatrixEngine& b, double tolerance) {
    if (a.rows != b.rows || a.cols != b.cols) {
        return false;
    }
    
    return (a.matrix - b.matrix).norm() < tolerance;
}
