#include "MatrixEngineAdapter.h"
#include <cmath>
#include <algorithm>
#include <stdexcept>
#include <limits>

// Basic Operations
Matrix MatrixEngineAdapter::add(const Matrix &a, const Matrix &b)
{
    validateDimensions(a, b, "addition");
    
    Matrix result(a.rows, a.cols);
    for (int i = 0; i < a.rows; ++i) {
        for (int j = 0; j < a.cols; ++j) {
            result.data[i][j] = a.data[i][j] + b.data[i][j];
        }
    }
    return result;
}

Matrix MatrixEngineAdapter::subtract(const Matrix &a, const Matrix &b)
{
    validateDimensions(a, b, "subtraction");
    
    Matrix result(a.rows, a.cols);
    for (int i = 0; i < a.rows; ++i) {
        for (int j = 0; j < a.cols; ++j) {
            result.data[i][j] = a.data[i][j] - b.data[i][j];
        }
    }
    return result;
}

Matrix MatrixEngineAdapter::multiply(const Matrix &a, const Matrix &b)
{
    if (a.cols != b.rows) {
        throw std::invalid_argument("Matrix dimensions incompatible for multiplication");
    }
    
    Matrix result(a.rows, b.cols);
    for (int i = 0; i < a.rows; ++i) {
        for (int j = 0; j < b.cols; ++j) {
            double sum = 0.0;
            for (int k = 0; k < a.cols; ++k) {
                sum += a.data[i][k] * b.data[k][j];
            }
            result.data[i][j] = sum;
        }
    }
    return result;
}

Matrix MatrixEngineAdapter::transpose(const Matrix &a)
{
    Matrix result(a.cols, a.rows);
    for (int i = 0; i < a.rows; ++i) {
        for (int j = 0; j < a.cols; ++j) {
            result.data[j][i] = a.data[i][j];
        }
    }
    return result;
}

Matrix MatrixEngineAdapter::inverse(const Matrix &a)
{
    validateSquare(a, "inverse");
    
    int n = a.rows;
    Matrix augmented(n, 2 * n);
    
    // Create augmented matrix [A | I]
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            augmented.data[i][j] = a.data[i][j];
            augmented.data[i][j + n] = (i == j) ? 1.0 : 0.0;
        }
    }
    
    // Gauss-Jordan elimination
    for (int i = 0; i < n; ++i) {
        // Find pivot
        int maxRow = i;
        for (int k = i + 1; k < n; ++k) {
            if (std::abs(augmented.data[k][i]) > std::abs(augmented.data[maxRow][i])) {
                maxRow = k;
            }
        }
        
        if (std::abs(augmented.data[maxRow][i]) < 1e-10) {
            throw std::runtime_error("Matrix is singular (not invertible)");
        }
        
        // Swap rows
        std::swap(augmented.data[i], augmented.data[maxRow]);
        
        // Scale pivot row
        double pivot = augmented.data[i][i];
        for (int j = 0; j < 2 * n; ++j) {
            augmented.data[i][j] /= pivot;
        }
        
        // Eliminate column
        for (int k = 0; k < n; ++k) {
            if (k != i) {
                double factor = augmented.data[k][i];
                for (int j = 0; j < 2 * n; ++j) {
                    augmented.data[k][j] -= factor * augmented.data[i][j];
                }
            }
        }
    }
    
    // Extract inverse from right half
    Matrix result(n, n);
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            result.data[i][j] = augmented.data[i][j + n];
        }
    }
    
    return result;
}

// Properties
double MatrixEngineAdapter::determinant(const Matrix &a)
{
    validateSquare(a, "determinant");
    
    int n = a.rows;
    Matrix temp = a;
    double det = 1.0;
    
    for (int i = 0; i < n; ++i) {
        // Find pivot
        int maxRow = i;
        for (int k = i + 1; k < n; ++k) {
            if (std::abs(temp.data[k][i]) > std::abs(temp.data[maxRow][i])) {
                maxRow = k;
            }
        }
        
        if (std::abs(temp.data[maxRow][i]) < 1e-10) {
            return 0.0;
        }
        
        if (maxRow != i) {
            std::swap(temp.data[i], temp.data[maxRow]);
            det *= -1.0;
        }
        
        det *= temp.data[i][i];
        
        // Eliminate column
        for (int k = i + 1; k < n; ++k) {
            double factor = temp.data[k][i] / temp.data[i][i];
            for (int j = i; j < n; ++j) {
                temp.data[k][j] -= factor * temp.data[i][j];
            }
        }
    }
    
    return det;
}

double MatrixEngineAdapter::trace(const Matrix &a)
{
    validateSquare(a, "trace");
    
    double sum = 0.0;
    for (int i = 0; i < a.rows; ++i) {
        sum += a.data[i][i];
    }
    return sum;
}

int MatrixEngineAdapter::rank(const Matrix &a)
{
    Matrix temp = a;
    int rank = 0;
    int rows = a.rows;
    int cols = a.cols;
    
    for (int col = 0; col < cols && rank < rows; ++col) {
        // Find pivot
        int pivotRow = rank;
        for (int row = rank + 1; row < rows; ++row) {
            if (std::abs(temp.data[row][col]) > std::abs(temp.data[pivotRow][col])) {
                pivotRow = row;
            }
        }
        
        if (std::abs(temp.data[pivotRow][col]) < 1e-10) {
            continue;
        }
        
        if (pivotRow != rank) {
            std::swap(temp.data[rank], temp.data[pivotRow]);
        }
        
        // Eliminate
        for (int row = rank + 1; row < rows; ++row) {
            double factor = temp.data[row][col] / temp.data[rank][col];
            for (int j = col; j < cols; ++j) {
                temp.data[row][j] -= factor * temp.data[rank][j];
            }
        }
        
        rank++;
    }
    
    return rank;
}

double MatrixEngineAdapter::norm(const Matrix &a)
{
    // Frobenius norm
    double sum = 0.0;
    for (int i = 0; i < a.rows; ++i) {
        for (int j = 0; j < a.cols; ++j) {
            sum += a.data[i][j] * a.data[i][j];
        }
    }
    return std::sqrt(sum);
}

double MatrixEngineAdapter::condition(const Matrix &a)
{
    validateSquare(a, "condition number");
    
    try {
        Matrix inv = inverse(a);
        return norm(a) * norm(inv);
    } catch (...) {
        return std::numeric_limits<double>::infinity();
    }
}

// Decompositions
std::pair<Matrix, Matrix> MatrixEngineAdapter::luDecomposition(const Matrix &a)
{
    validateSquare(a, "LU decomposition");
    
    int n = a.rows;
    Matrix L = createIdentity(n);
    Matrix U = a;
    
    for (int i = 0; i < n - 1; ++i) {
        for (int j = i + 1; j < n; ++j) {
            if (std::abs(U.data[i][i]) < 1e-10) {
                throw std::runtime_error("LU decomposition failed (zero pivot)");
            }
            
            double factor = U.data[j][i] / U.data[i][i];
            L.data[j][i] = factor;
            
            for (int k = i; k < n; ++k) {
                U.data[j][k] -= factor * U.data[i][k];
            }
        }
    }
    
    return {L, U};
}

std::pair<Matrix, Matrix> MatrixEngineAdapter::qrDecomposition(const Matrix &a)
{
    int m = a.rows;
    int n = a.cols;
    
    Matrix Q(m, n);
    Matrix R(n, n);
    
    // Gram-Schmidt process
    for (int j = 0; j < n; ++j) {
        // Extract column j
        std::vector<double> v(m);
        for (int i = 0; i < m; ++i) {
            v[i] = a.data[i][j];
        }
        
        // Orthogonalize against previous columns
        for (int k = 0; k < j; ++k) {
            double dotProduct = 0.0;
            for (int i = 0; i < m; ++i) {
                dotProduct += Q.data[i][k] * v[i];
            }
            R.data[k][j] = dotProduct;
            
            for (int i = 0; i < m; ++i) {
                v[i] -= dotProduct * Q.data[i][k];
            }
        }
        
        // Normalize
        double norm = vectorNorm(v);
        R.data[j][j] = norm;
        
        if (norm > 1e-10) {
            for (int i = 0; i < m; ++i) {
                Q.data[i][j] = v[i] / norm;
            }
        }
    }
    
    return {Q, R};
}

std::vector<double> MatrixEngineAdapter::eigenvalues(const Matrix &a)
{
    validateSquare(a, "eigenvalues");
    
    // Simple power iteration for demonstration
    // For production, use proper eigenvalue algorithms (QR algorithm, etc.)
    int n = a.rows;
    std::vector<double> eigenvals;
    
    // This is a simplified placeholder
    // Real implementation would use QR algorithm or similar
    for (int i = 0; i < n; ++i) {
        eigenvals.push_back(a.data[i][i]); // Diagonal elements as rough estimate
    }
    
    return eigenvals;
}

// Private helper methods
void MatrixEngineAdapter::validateDimensions(const Matrix &a, const Matrix &b, const std::string &op)
{
    if (a.rows != b.rows || a.cols != b.cols) {
        throw std::invalid_argument("Matrix dimensions must match for " + op);
    }
}

void MatrixEngineAdapter::validateSquare(const Matrix &a, const std::string &op)
{
    if (a.rows != a.cols) {
        throw std::invalid_argument("Matrix must be square for " + op);
    }
}

Matrix MatrixEngineAdapter::createIdentity(int size)
{
    Matrix I(size, size);
    for (int i = 0; i < size; ++i) {
        I.data[i][i] = 1.0;
    }
    return I;
}

double MatrixEngineAdapter::vectorNorm(const std::vector<double> &v)
{
    double sum = 0.0;
    for (double val : v) {
        sum += val * val;
    }
    return std::sqrt(sum);
}
