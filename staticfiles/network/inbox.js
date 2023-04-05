function edit_post(x) {
    fetch(`/edit/${x}`)
    .then(response => response.json())
    .then(post => {
        console.log(post)
        const div = document.getElementsByClassName(`${post.id}`)[0];
        const text = div.querySelector(':scope > .div2 > .for_edit > .content');
        text.remove();
        const new_text = document.createElement('textarea');
        new_text.innerHTML = `${post.content}`;
        new_text.setAttribute('id', 'new_text');
        new_text.style.cssText = 'width: 100%; border: 1px solid GainsBoro';

        const poster = div.querySelector(':scope > .div2 > .for_edit');
        poster.appendChild(new_text);

        const save_button = document.createElement('button');
        save_button.innerHTML = 'Save';
        save_button.setAttribute('id', 'save_button');
        save_button.className = 'btn btn-success';
        save_button.onclick = function() {
            save_changes(x, new_text.value)
        };
        poster.appendChild(save_button);
    })
};


function save_changes(a, b) {
    fetch(`/edit/${a}`, {
        method: 'PUT',
        body: JSON.stringify({
            content: b
        })
    })
    .then(response => response.json())
    .then(post => {
        console.log(post)
        const div = document.getElementsByClassName(`${post.id}`)[0];
        const old_text = div.querySelector(':scope > .div2 > .for_edit > #new_text');
        const old_button = div.querySelector(':scope > .div2 > .for_edit > #save_button');
        old_text.remove();
        old_button.remove();
        const edited_post = document.createElement('p');
        edited_post.className = 'content';
        edited_post.style.cssText = 'font-size: 20px';
        edited_post.innerHTML = `"${post.content}"`;
        const poster = div.querySelector(':scope > .div2 > .for_edit');
        poster.appendChild(edited_post);
    })
}


function delete_post(x) {
    document.addEventListener('click', event => {
        const element = event.target;

        if (element.id === 'delete') {
            element.parentElement.parentElement.style.animationPlayState = 'running';
            element.parentElement.parentElement.addEventListener('animationed', () => {
                element.parentElement.parentElement.remove();
            })
        }
    })
    fetch(`/delete/${x}`)
}

function count_likes(x) {
    fetch(`/likes/${x}`)
    .then(response => response.json())
    .then(post => {
        console.log(post)
        const div = document.getElementsByClassName(`${post.id}`)[0];
        const update_likes = div.querySelector(':scope > .div2 > .likes');
        update_likes.innerHTML = post.likes;
        const button = div.querySelector(':scope > .div2 > #likes');
        if (button.innerText === '\u2665') {
            button.innerHTML = '&#x2661;';
        } else {
            button.innerHTML = '&#x2665;';
        }
    })
}


function change_follow(a) {
    fetch(`/follow/${a}`)
    .then(response => response.json())
    .then(data => {
        console.log(data);
        const followers = document.querySelector('#followers');
        followers.innerHTML = `Followers: ${data.followers}`;
    })
}


function view_comment(a) {
    const div = document.getElementsByClassName(`${a}`)[0];
    const actual_div = div.querySelector(':scope > .div2 > .view_all_comment');
    if (actual_div.style.display === 'none') {
        actual_div.style.display = 'block'
    } else {
        actual_div.style.display = 'none'
    }
}


function add_comment(a) {
    const div = document.getElementsByClassName(`${a}`)[0];
    const new_comment = div.querySelector(':scope > .div2 > .view_all_comment > .new > input');
    const new_comment_value = new_comment.value;

    fetch(`/add_comment/${a}`, {
        method: 'PUT',
        body: JSON.stringify({
            content: new_comment_value
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        const list = div.querySelector(':scope > .div2 > .view_all_comment > .ul');
        const list_to_add = document.createElement('li');
        list_to_add.innerHTML = `<a href="{% url 'profile' data.commentor.id %}">${data.commentor}</a>: <strong>${data.comment}</strong>(${data.time})
        <button type="button" style="font-size:10px" class="btn btn-link" onclick="delete_comment(${ data.id }, ${a})">[delete]</button>`
        list.appendChild(list_to_add);
        list_to_add.className = `${data.id}`;
        fetch(`/add_comment/${a}`)
        .then(response => response.json())
        .then(new_data => {
            console.log(new_data);
            const comments_amount = new_data.comments_amount;
            const button = div.querySelector(':scope > .div2 > #comment_button');
            button.innerHTML = `View & Add Comments(${comments_amount})`
        })
    })
    new_comment.value = ''
}


function delete_comment(comment_id, post_id) {
    const li = document.getElementsByClassName(`${comment_id}`)[0];
    li.remove();

    fetch(`/delete_comment/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            content: comment_id
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        const comments_amount = data.comments_amount;
        const div = document.getElementsByClassName(`${post_id}`)[0];
        const button = div.querySelector(':scope > .div2 > #comment_button');
        button.innerHTML = `View & Add Comments(${comments_amount})`
    });
}

document.addEventListener('click', event => {
    const element = event.target;

    if (element.id === 'delete') {
        element.parentElement.parentElement.style.animationPlayState = 'running';
        element.parentElement.parentElement.addEventListener('animationed', () => {
            element.parentElement.parentElement.remove();
        })
    }
})