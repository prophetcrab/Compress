#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <queue>
#include <unordered_map>
#include <vector>
#include <string>

namespace py = pybind11;

// 节点结构体
struct Node {
    char ch;
    int freq;
    Node* left;
    Node* right;

    Node(char ch, int freq) : ch(ch), freq(freq), left(nullptr), right(nullptr) {}
};

void freeTree(Node* root);

// 比较节点的频率
struct Compare {
    bool operator()(Node* left, Node* right) {
        return left->freq > right->freq;
    }
};

// 生成霍夫曼树
Node* buildHuffmanTree(const std::unordered_map<unsigned char, int>& freqMap) {
    std::priority_queue<Node*, std::vector<Node*>, Compare> pq;

    for (auto pair : freqMap) {
        pq.push(new Node(pair.first, pair.second));
    }

    while (pq.size() != 1) {
        Node* left = pq.top(); pq.pop();
        Node* right = pq.top(); pq.pop();

        int sum = left->freq + right->freq;
        Node* newNode = new Node('\0', sum);
        newNode->left = left;
        newNode->right = right;

        pq.push(newNode);
    }

    return pq.top();
}

// 生成霍夫曼编码表
void generateCodes(Node* root, const std::string& str, std::unordered_map<unsigned char, std::string>& huffmanCode) {
    if (root == nullptr) {
        return;
    }

    if (!root->left && !root->right) {
        huffmanCode[(unsigned char)root->ch] = str;
    }

    generateCodes(root->left, str + "0", huffmanCode);
    generateCodes(root->right, str + "1", huffmanCode);
}

// 编码字节数据
std::string encode(const std::vector<unsigned char>& data, std::unordered_map<unsigned char, std::string>& huffmanCode) {
    std::unordered_map<unsigned char, int> freqMap;
    for (unsigned char byte : data) {
        freqMap[byte]++;
    }

    Node* root = buildHuffmanTree(freqMap);
    generateCodes(root, "", huffmanCode);

    std::string encodedStr = "";
    for (unsigned char byte : data) {
        encodedStr += huffmanCode.at(byte);
    }

    // 清理树
    freeTree(root);

    return encodedStr;
}

// 生成解码表
std::unordered_map<std::string, unsigned char> generateDecodeMap(const std::unordered_map<unsigned char, std::string>& huffmanCode) {
    std::unordered_map<std::string, unsigned char> decodeMap;
    for (const auto& pair : huffmanCode) {
        decodeMap[pair.second] = pair.first;
    }
    return decodeMap;
}

// 解码字符串
std::vector<unsigned char> decode(const std::unordered_map<std::string, unsigned char>& decodeMap, const std::string& encodedStr) {
    std::vector<unsigned char> decodedData;
    std::string currentCode = "";

    for (char bit : encodedStr) {
        currentCode += bit;
        if (decodeMap.find(currentCode) != decodeMap.end()) {
            decodedData.push_back(decodeMap.at(currentCode));
            currentCode = "";
        }
    }
    return decodedData;
}

// 清理霍夫曼树
void freeTree(Node* root) {
    if (root == nullptr) {
        return;
    }
    freeTree(root->left);
    freeTree(root->right);
    delete root;
}



// 通过 pybind11 暴露给 Python
PYBIND11_MODULE(huffman, m) {
    m.def("encode", [](const std::vector<unsigned char> &data) {
        std::unordered_map<unsigned char, std::string> huffmanCode;
        std::string encodedStr = encode(data, huffmanCode);
        return py::make_tuple(encodedStr, huffmanCode);
    });

    m.def("decode", &decode);
    m.def("generate_decode_map", &generateDecodeMap);
}
