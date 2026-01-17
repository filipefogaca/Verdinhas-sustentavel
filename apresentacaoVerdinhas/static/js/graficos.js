document.addEventListener('DOMContentLoaded', function() {
    // Só executa o código se houver um elemento <canvas> na página
    if (!document.querySelector('canvas')) {
        return;
    }

    // --- OPÇÕES GLOBAIS PARA OS GRÁFICOS ---
    const globalChartOptions = {
        responsive: true,
        animation: {
            duration: 1000,
            easing: 'easeInOutQuart'
        },
        plugins: {
            legend: {
                display: false
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    display: false,
                    drawBorder: false
                }
            },
            x: {
                grid: {
                    display: false,
                    drawBorder: false
                }
            }
        }
    };


    fetch('/api/dados')
        .then(response => response.json())
        .then(dados => {

            // --- GRÁFICOS PARA pagina2.html ---
           // EM static/js/graficos.js

// --- GRÁFICOS PARA pagina2.html (COM ANIMAÇÃO DE DESENHO) ---
const ctxBrasil = document.getElementById('graficoLixoBrasil');
if (ctxBrasil) {
    new Chart(ctxBrasil, {
        type: 'line',
        data: {
            labels: dados.lixoBrasil.labels,
            datasets: [{
                data: dados.lixoBrasil.data,
                borderColor: 'rgb(0, 123, 255)',
                backgroundColor: 'rgba(0, 123, 255, 0.1)',
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            ...globalChartOptions, // Mantém as opções globais
            scales: {
                ...globalChartOptions.scales, // Mantém as opções dos eixos
                y: { // Sobrescreve apenas a configuração do eixo Y
                    ...globalChartOptions.scales.y,
                    min: 60 // <<-- AQUI ESTÁ A MUDANÇA
                }
            },
            animation: { // A animação de desenho continua a mesma
                x: {
                    type: 'number', easing: 'linear', duration: 1000, from: NaN,
                    delay(ctx) { if (ctx.type !== 'data' || ctx.xStarted) { return 0; } ctx.xStarted = true; return ctx.index * 100; }
                },
                y: {
                    type: 'number', easing: 'linear', duration: 1000,
                    from: (ctx) => { if (ctx.type === 'data') { const prev = ctx.chart.getDatasetMeta(ctx.datasetIndex).data[ctx.index - 1]; return prev ? prev.y : 50; } } // Ajustado para começar a animação de 50
                }
            }
        }
    });
}

const ctxGlobal = document.getElementById('graficoLixoGlobal');
if (ctxGlobal) {
    new Chart(ctxGlobal, {
        type: 'line',
        data: {
            labels: dados.lixoGlobal.labels,
            datasets: [{
                data: dados.lixoGlobal.data,
                borderColor: 'rgb(40, 167, 69)',
                backgroundColor: 'rgba(40, 167, 69, 0.1)',
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            ...globalChartOptions,
            scales: {
                ...globalChartOptions.scales,
                y: {
                    ...globalChartOptions.scales.y,
                    min: 1.4 // <<-- AQUI ESTÁ A MUDANÇA
                }
            },
            animation: { // A mesma animação de desenho
                x: {
                    type: 'number', easing: 'linear', duration: 1000, from: NaN,
                    delay(ctx) { if (ctx.type !== 'data' || ctx.xStarted) { return 0; } ctx.xStarted = true; return ctx.index * 100; }
                },
                y: {
                    type: 'number', easing: 'linear', duration: 1000,
                    from: (ctx) => { if (ctx.type === 'data') { const prev = ctx.chart.getDatasetMeta(ctx.datasetIndex).data[ctx.index - 1]; return prev ? prev.y : 1.0; } } // Ajustado para começar a animação de 1.0
                }
            }
        }
    });
}

            // --- GRÁFICOS PARA pagina3.html ---
            const ctxAmbiental = document.getElementById('graficoImpactoAmbiental');
            if (ctxAmbiental) {
                new Chart(ctxAmbiental, {
                    type: 'pie',
                    data: {
                        labels: dados.impactoAmbiental.labels,
                        datasets: [{
                            data: dados.impactoAmbiental.data,
                            backgroundColor: ['#ff6384', '#36a2eb', '#ffce56', '#4bc0c0']
                        }]
                    },
                    options: {
                        responsive: true,
                        animation: { duration: 1000, easing: 'easeInOutQuart' },
                        plugins: {
                            title: { display: true, text: 'Participação dos Resíduos na Emissão de Metano (%)' }
                        }
                    }
                });
            }

            const ctxSocial = document.getElementById('graficoImpactoSocial');
            if (ctxSocial) {
                new Chart(ctxSocial, {
                    type: 'bar',
                    data: {
                        labels: dados.impactoSocial.labels,
                        datasets: [{
                            data: dados.impactoSocial.data,
                            backgroundColor: ['#36a2eb', '#ff6384']
                        }]
                    },
                    options: {
                        ...globalChartOptions,
                        indexAxis: 'y',
                        plugins: { ...globalChartOptions.plugins, title: { display: true, text: 'Prevalência de Sintomas Respiratórios (%)' } }
                    }
                });
            }

            // EM static/js/graficos.js

// CÓDIGO FINAL, SIMPLES E CORRETO
const ctxEconomico = document.getElementById('graficoImpactoEconomico');
if (ctxEconomico) {
    new Chart(ctxEconomico, {
        type: 'bar',
        data: {
            labels: dados.impactoEconomico.labels, // Agora ele recebe os arrays de strings
            datasets: [{
                data: dados.impactoEconomico.data,
                backgroundColor: ['#ffce56', '#ff6384']
            }]
        },
        options: {
            ...globalChartOptions, // Usa as opções globais (sem grades, com animação)
            plugins: {
                ...globalChartOptions.plugins,
                title: { display: true, text: 'Valor (em Bilhões de R$)' }
            }
        }
    });
}



            // --- GRÁFICOS PARA pagina_alerta.html ---
            const ctxDecomposicao = document.getElementById('graficoDecomposicao');
            if (ctxDecomposicao) {
                new Chart(ctxDecomposicao, {
                    type: 'bar',
                    data: {
                        labels: dados.decomposicao.labels,
                        datasets: [{
                            data: dados.decomposicao.data,
                            backgroundColor: '#dc3545'
                        }]
                    },
                    options: {
                        ...globalChartOptions,
                        indexAxis: 'y',
                        scales: {
                            x: {
                                type: 'logarithmic',
                                title: { display: true, text: 'Anos (Escala Logarítmica)' },
                                grid: { display: false, drawBorder: false }
                            },
                            y: { grid: { display: false, drawBorder: false } }
                        },
                        plugins: {
                            ...globalChartOptions.plugins,
                            tooltip: {
                                callbacks: { label: (context) => ' ' + context.raw + ' anos' }
                            }
                        }
                    }
                });
            }

            const ctxReciclagem = document.getElementById('graficoReciclagem');
            if (ctxReciclagem) {
                const backgroundColors = dados.taxaReciclagem.labels.map(label =>
                    label === 'Brasil' ? '#ffc107' : '#007bff'
                );
                new Chart(ctxReciclagem, {
                    type: 'bar',
                    data: {
                        labels: dados.taxaReciclagem.labels,
                        datasets: [{
                            data: dados.taxaReciclagem.data,
                            backgroundColor: backgroundColors
                        }]
                    },
                    options: {
                        ...globalChartOptions,
                        plugins: { ...globalChartOptions.plugins, title: { display: true, text: 'Taxa de Reciclagem (%)' } }
                    }
                });
            }
        });
});
