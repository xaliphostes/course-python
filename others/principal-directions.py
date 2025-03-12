import numpy as np

def compute_principal_directions(tensor):
    """
    Compute the principal directions of a 2D tensor.
    
    Parameters:
    -----------
    tensor : array_like
        A 2x2 tensor (symmetric matrix)
    
    Returns:
    --------
    eigenvalues : ndarray
        The eigenvalues of the tensor
    eigenvectors : ndarray
        The eigenvectors of the tensor, each column is an eigenvector
    """
    # Ensure the tensor is symmetric (as it should be for physical tensors)
    if not np.allclose(tensor, tensor.T):
        raise ValueError("Tensor must be symmetric")
    
    # Compute eigenvalues and eigenvectors
    eigenvalues, eigenvectors = np.linalg.eigh(tensor)
    
    # Sort eigenvalues and eigenvectors in descending order
    idx = eigenvalues.argsort()[::-1]
    eigenvalues = eigenvalues[idx]
    eigenvectors = eigenvectors[:, idx]
    
    return eigenvalues, eigenvectors

# Example usage
if __name__ == "__main__":
    # Example 2D tensor (stress tensor, strain tensor, etc.)
    tensor = np.array([
        [3.0, 1.0],
        [1.0, 2.0]
    ])
    
    eigenvalues, eigenvectors = compute_principal_directions(tensor)
    # eigenvalues, eigenvectors = np.linalg.eigh(tensor)
    
    print("Eigenvalues (principal values):")
    print(eigenvalues)
    
    print("\nEigenvectors (principal directions):")
    print(eigenvectors)
    
    print("\nFirst principal direction:")
    print(eigenvectors[:, 0])
    
    print("\nSecond principal direction:")
    print(eigenvectors[:, 1])