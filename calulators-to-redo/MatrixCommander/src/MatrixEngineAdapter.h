#ifndef MATRIXENGINE_ADAPTER_H
#define MATRIXENGINE_ADAPTER_H

#include <vector>
#include <string>
#include <QString>

// Simple Matrix structure for UI compatibility
struct Matrix {
    int rows = 0;
    int cols = 0;
    std::vector<std::vector<double>> data;
    
    Matrix() = default;
    Matrix(int r, int c) : rows(r), cols(c), data(r, std::vector<double>(c, 0.0)) {}
};

// Helper function to format matrix for display
inline QString formatMatrix(const Matrix &m) {
    QString result;
    for (int i = 0; i < m.rows; ++i) {
        QString row = "║   ";
        for (int j = 0; j < m.cols; ++j) {
            row += QString("%1 ").arg(m.data[i][j], 8, 'f', 3);
        }
        while (row.length() < 39) row += " ";
        row += "║\n";
        result += row;
    }
    return result;
}

// MatrixEngine interface for UI
class MatrixEngineAdapter
{
public:
    MatrixEngineAdapter() = default;
    
    // Basic Operations
    Matrix add(const Matrix &a, const Matrix &b);
    Matrix subtract(const Matrix &a, const Matrix &b);
    Matrix multiply(const Matrix &a, const Matrix &b);
    Matrix transpose(const Matrix &a);
    Matrix inverse(const Matrix &a);
    
    // Properties
    double determinant(const Matrix &a);
    double trace(const Matrix &a);
    int rank(const Matrix &a);
    double norm(const Matrix &a);
    double condition(const Matrix &a);
    
    // Decompositions
    std::pair<Matrix, Matrix> luDecomposition(const Matrix &a);
    std::pair<Matrix, Matrix> qrDecomposition(const Matrix &a);
    std::vector<double> eigenvalues(const Matrix &a);
    
private:
    void validateDimensions(const Matrix &a, const Matrix &b, const std::string &op);
    void validateSquare(const Matrix &a, const std::string &op);
    Matrix createIdentity(int size);
    double vectorNorm(const std::vector<double> &v);
};

#endif // MATRIXENGINE_ADAPTER_H
