package com.example.cadastros

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.tooling.preview.Preview

// Função de validação
fun isValid(nome: String, quantidade: Int, precoCusto: String, precoVenda: String): Boolean {
    val precoCustoValido = precoCusto.isEmpty() || (precoCusto.toDoubleOrNull() ?: -1.0) > 0
    return nome.length > 3 &&
            quantidade > 0 &&
            precoCustoValido &&
            (precoVenda.toDoubleOrNull() ?: -1.0) > 0
}

// Classe Produto
data class Produto(
    val nome: String,
    val quantidade: Int,
    val precoCusto: Double?,
    val precoVenda: Double,
    val marca: String?
)

@Composable
fun CadastroProdutoScreen() {

    var nomeProduto by remember { mutableStateOf("") }
    var quantidade by remember { mutableStateOf("") }
    var precoCusto by remember { mutableStateOf("") }
    var precoVenda by remember { mutableStateOf("") }
    var marca by remember { mutableStateOf("") }

    var errorMessage by remember { mutableStateOf("") }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        // Título
        Text(
            text = "Cadastro de produto",
            fontSize = 24.sp,
            modifier = Modifier
                .padding(top = 16.dp, start = 8.dp)
        )

        Spacer(modifier = Modifier.height(24.dp))

        // Nome do produto
        OutlinedTextField(
            value = nomeProduto,
            onValueChange = { nomeProduto = it },
            label = { Text("Nome do produto") },
            keyboardOptions = KeyboardOptions.Default,
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(modifier = Modifier.height(16.dp))

        // Quantidade em estoque
        OutlinedTextField(
            value = quantidade,
            onValueChange = { quantidade = it },
            label = { Text("Quantidade em estoque") },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(modifier = Modifier.height(16.dp))

        // Preço de custo
        OutlinedTextField(
            value = precoCusto,
            onValueChange = { precoCusto = it },
            label = { Text("Preço de custo") },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(modifier = Modifier.height(16.dp))

        // Preço de venda
        OutlinedTextField(
            value = precoVenda,
            onValueChange = { precoVenda = it },
            label = { Text("Preço de venda") },
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
            modifier = Modifier.fillMaxWidth()
        )

        Spacer(modifier = Modifier.height(16.dp))

        // Nome da marca
        OutlinedTextField(
            value = marca,
            onValueChange = { marca = it },
            label = { Text("Nome da marca") },
            keyboardOptions = KeyboardOptions.Default,
            modifier = Modifier.fillMaxWidth()
        )

        // Exibindo mensagem de erro
        if (errorMessage.isNotEmpty()) {
            Text(
                text = errorMessage,
                color = MaterialTheme.colorScheme.error,
                modifier = Modifier.padding(top = 8.dp)
            )
        }

        Spacer(modifier = Modifier.height(32.dp))

        // Botões
        Row(
            horizontalArrangement = Arrangement.SpaceEvenly,
            modifier = Modifier.fillMaxWidth()
        ) {
            Button(onClick = {
                // Converte os valores para os tipos adequados
                val qtd = quantidade.toIntOrNull() ?: -1
                val custo = precoCusto.toDoubleOrNull()
                val venda = precoVenda.toDoubleOrNull() ?: -1.0

                val produto = Produto(
                    nome = nomeProduto.trim(),
                    quantidade = qtd,
                    precoCusto = custo,
                    precoVenda = venda,
                    marca = if (marca.isBlank()) null else marca.trim()
                )
                println("Nome do Produto: ${produto.nome}")
                println("Quantidade: ${produto.quantidade}")
                println("Preço de Custo: ${produto.precoCusto}")
                println("Preço de Venda: ${produto.precoVenda}")
                println("Marca: ${produto.marca}")

                // Valida o produto
                if (isValid(produto.nome, produto.quantidade, precoCusto, precoVenda)) {
                    // Produto válido, prossiga com o cadastro
                    errorMessage = "" // Limpa a mensagem de erro
                    println("Produto válido: $produto")
                } else {
                    // Produto inválido, exibe a mensagem de erro
                    errorMessage = "Por favor, preencha todos os campos corretamente."
                }
            }) {
                Text("Salvar")
            }

            OutlinedButton(onClick = {
                // Ação de cancelar
            }) {
                Text("Cancelar")
            }
        }

    }
}

@Preview(showBackground = true)
@Composable
fun CadastroProdutoPreview() {
    CadastroProdutoScreen()
}
